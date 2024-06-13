import eventlet
import json
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from user import *
import socket
import pdfkit
import sqlite3
from dbhandler import *
from fpdf import FPDF
import math
from subprocess import Popen
import sys
import time
import datetime
import os
from ToolHandler import *
import ssl

if os.path.exists("/home/jackfruit/ncs/BootTime.txt"):
    with open("/home/jackfruit/ncs/BootTime.txt", 'r') as f:
        boottime = f.read().strip()
    print("booted:", boottime)
else:
    boottime = "2020-04-14 15:03:26"

try:
    cleandata()
except Exception as e:
    print(e)

booted = False
eventlet.monkey_patch()

# Initialize MQTT broker settings
mqtt_broker_url = '5ccaf87576e04605a3c0b13e35dd0680.s1.eu.hivemq.cloud'
mqtt_broker_port = 8883
mqtt_username = 'jerish716'
mqtt_password = 'jerish716'
mqtt_topic = 'my/test/topic'
mqtt_topic_light = 'topic_light'

page_zoom = readsetting("pagezoom")
DB_Name = readsetting("datafarm")
activeData = {}

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = mqtt_broker_url
app.config['MQTT_BROKER_PORT'] = mqtt_broker_port
app.config['MQTT_USERNAME'] = mqtt_username
app.config['MQTT_PASSWORD'] = mqtt_password
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = True
app.config['MQTT_CLIENT_ID'] = 'rpibroker'
app.config['MQTT_TLS_VERSION'] = ssl.PROTOCOL_TLS  # Use highest TLS version

mqtt = Mqtt(app)
socketio = SocketIO(app)
BxSwitches, tdev = Switch_IDandCount()

for boxid, clid in BxSwitches.items():
    if boxid not in activeData.keys():
        activeData[boxid] = {}
    for client in clid:
        if client not in activeData[boxid].keys():
            activeData[boxid][client] = False

audFiles = {}
for i in range(1, tdev + 1):
    audFiles[str(i)] = "cust_sound/" + str(i) + ".mp3"
audFiles[str(tdev + 1)] = "sound/bell.mp3"

print(BxSwitches)

# Subscribe to MQTT topics
mqtt.subscribe(mqtt_topic, 1)
mqtt.subscribe('Tool/ToolData')

@app.route('/shutdown')
def shutdown():
    from subprocess import call
    call("sudo shutdown -h now", shell=True)
    return "shutting down now........"

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == "POST":
        ajxdata = json.loads(request.get_data().decode())
        if ajxdata['dataFrom'] == "Zoom":
            zoomdata = int(ajxdata["value"]) / 100
            setsetting("pagezoom", str(zoomdata))
            socketio.emit('reload', data="Reload")
        if ajxdata['dataFrom'] == "Time":
            datetime1 = ajxdata["value"]
            date, time = datetime1.split('T')
            datetimedata = "\"" + date + " " + time + "\""
            p = Popen("sudo date -s " + datetimedata, shell=True)
            p.wait()
            p = Popen("sudo hwclock -w", shell=True)
            p.wait()
            with open("/home/jackfruit/ncs/BootTime.txt", "w") as f:
                f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    zoomvalue = int(float(readsetting("pagezoom")) * 100)
    Currentdate = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    return render_template('settings.html', zoomvalue=str(zoomvalue), datenow=Currentdate)

@app.route('/report')
def mpdf():
    duration = readsetting("esc_duration")
    return render_template('report.html', data=retrivedatafromDB(duration))

@app.route('/reboot')
def reboot():
    from subprocess import call
    call("sudo reboot now", shell=True)
    return "restarting now........"

@app.route('/devop')
def devop():
    global activeData
    global audFiles
    actualbedcount = int(readsetting("beds"))
    dsptxt = retrivebednaming()
    BxSwitches, tdev = Switch_IDandCount()
    noofcolumn = int(readsetting("tablecolumn"))
    actualbedcount = int(readsetting("beds"))
    ToiletSwitchs = int(readsetting("Tlight"))
    totalbed = (math.ceil(actualbedcount / noofcolumn)) * noofcolumn
    loopvalue = totalbed + 1
    dsptxt = retrivebednaming()
    totalaudFiles = actualbedcount + ToiletSwitchs
    return BxSwitches

@app.route('/refreshdata')
def refreshdata():
    global activeData
    for boxs in activeData.keys():
        for ids in activeData[boxs].keys():
            activeData[boxs][ids] = False
    return "Successfull" + str(activeData)

@app.route('/clearlogs')
def clearlogs():
    clearHistoryTable()
    return "Cleared Logs..!!"

@app.route('/')
def index():
    global activeData
    global booted
    global audFiles
    global tdev
    noofcolumn = int(readsetting("tablecolumn"))
    actualbedcount = int(readsetting("beds"))
    ToiletSwitchs = int(readsetting("Tlight"))
    totalbed = (math.ceil(actualbedcount / noofcolumn)) * noofcolumn
    loopvalue = totalbed + 1
    dsptxt = retrivebednaming()
    page_zoom = readsetting("pagezoom")
    booted = True
    return render_template('index.html', noofcolumn=noofcolumn, totalbed=totalbed, loopvalue=loopvalue, zommdata=page_zoom, actualbedcount=actualbedcount, dsptxt=dsptxt, audFiles=audFiles, BT_swcount=tdev + 1, BxSwitches=BxSwitches)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("mqtt connected")
    mqtt.subscribe(mqtt_topic, 1)
    mqtt.subscribe('Tool/ToolData')
    global booted
    booted = True  # Set booted to True once connected to the MQTT broker

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    try:
        global activeData
        global booted
        if not booted:
            print("NOT YET LOADED!!")
            return

        print(f"Received message: {message.payload} on topic: {message.topic}")

        # Ensure the topic has the correct format
        topic_parts = message.topic.split("/", 1)
        if len(topic_parts) != 2:
            print(f"Unexpected topic format: {message.topic}")
            return

        topictmp, clienttmp = topic_parts
        print(f"Topictmp: {topictmp}, Clienttmp: {clienttmp}")

        if topictmp == 'Tool' and clienttmp == 'ToolData':
            print("Data From Tool")
            jsonData = message.payload.decode()
            info = json.loads(jsonData)
            dbfile = info['appsetting']['DB_Name']
            ClearAllTables(dbfile)
            UpdateAllTables(dbfile, info)
            print("Done")
            socketio.emit('reload', data="Reload")
            from subprocess import call
            call("sudo reboot now", shell=True)
        else:
            # Retrieve box data
            modfiedboxdata = retrivebox(clienttmp)
            if not modfiedboxdata or len(modfiedboxdata) == 0:
                print(f"retrivebox() returned empty data for clienttmp: {clienttmp}")
                return

            client_id = modfiedboxdata[0][0]
            boxsuffix = modfiedboxdata[0][1][-1]
            if boxsuffix.isnumeric():
                boxsuffix = "-"

            print(f"Modified box data: {modfiedboxdata}")

            data = dict(
                topic=topictmp,
                client=client_id,
                boxname=modfiedboxdata[0][1],
                payload=message.payload.decode(),
                clientid=clienttmp,
                suffix=boxsuffix
            )

            print(f"Data: {data}")

            if data['payload'] in ["150", "210", "250"] and booted:
                if client_id in activeData:
                    activeData[client_id][clienttmp] = True
                else:
                    print(f"Client ID '{client_id}' not found in activeData")
            elif data['payload'] == "180" and booted:
                if client_id in activeData:
                    activeData[client_id][clienttmp] = False
                else:
                    print(f"Client ID '{client_id}' not found in activeData")

            data['Effect'] = any(activeData[client_id].values())
            socketio.emit('mqtt_message', data=data)

            t1 = datetime.datetime.strptime(boottime, "%Y-%m-%d %H:%M:%S")
            t2 = datetime.datetime.now()
            t3 = t2 - t1
            print(data)

    except Exception as e:
        print(f"Exception: {e}")










# @mqtt.on_log()
# def handle_logging(client, userdata, level, buf):
#     print("log: ", buf)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
