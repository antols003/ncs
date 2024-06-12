
import paho.mqtt.client as mqtt
import json
import os
from getmyip import get_ip
from ToolHandler import *
# MQTT Settings 
MQTT_Port = 1883
Keep_Alive_Interval = 45
mqtt_broker_ip=get_ip()
mqtt_topic='Tool/ToolData'
mqtt_username='oora' 
mqtt_password='oora'

#Subscribe to all Sensors at Base Topic
print ("connected...")
def on_connect(client, userdata, flags, rc):
    mqttc.subscribe(mqtt_topic)
    print ("connected...")

#Save Data into DB Table
def on_message(client, userdata, message):
    # This is the Master Call for saving MQTT Data into DB
    # For details of "sensor_Data_Handler" function please refer "sensor_data_to_db.py"
    topictmp,clienttmp=message.topic.split("/",1)
    data = dict(
        topic=topictmp,
        client=clienttmp,
        #topic=message.topic,
        status=message.payload.decode()
        #client=message.clientID
    )
    print("subscribing data")
    # print(type(data))
    
    jsonobj=json.dumps(data)
    # print(type(jsonobj))
    #print(jsonobj)
    res=json.loads(jsonobj)['status']
    info = json.loads(res)
    print(info['appsetting']['DB_Name'])
    dbfile=info['appsetting']['DB_Name']
    print("Done")
    ClearAllTables(dbfile)
    UpdateAllTables(dbfile,info)
    print("Done")

    #NCS_Trends_Data_Handler(data)
    #sensor_Data_Handler(data)



def on_subscribe(mosq, obj, mid, granted_qos):
    pass

mqttc = mqtt.Client()
mqttc.username_pw_set(mqtt_username, mqtt_password)
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe


# Connect
mqttc.connect(mqtt_broker_ip, int(MQTT_Port), int(Keep_Alive_Interval))

# Continue the network loop
mqttc.loop_forever()
