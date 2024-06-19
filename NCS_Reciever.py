
# import paho.mqtt.client as mqtt
# import json
# import os
# from getmyip import get_ip
# from ToolHandler import *
# # MQTT Settings 
# MQTT_Port = 8883
# Keep_Alive_Interval = 45
# mqtt_broker_ip='5ccaf87576e04605a3c0b13e35dd0680.s1.eu.hivemq.cloud:8884/mqtt'
# mqtt_topic='Tool/ToolData'
# mqtt_username='jerish716' 
# mqtt_password='jerish716'

# #Subscribe to all Sensors at Base Topic
# print ("connected...")
# def on_connect(client, userdata, flags, rc):
#     mqttc.subscribe(mqtt_topic)
#     print ("connected...")

# #Save Data into DB Table
# def on_message(client, userdata, message):
#     # This is the Master Call for saving MQTT Data into DB
#     # For details of "sensor_Data_Handler" function please refer "sensor_data_to_db.py"
#     topictmp,clienttmp=message.topic.split("/",1)
#     data = dict(
#         topic=topictmp,
#         client=clienttmp,
#         #topic=message.topic,
#         status=message.payload.decode()
#         #client=message.clientID
#     )
#     print("subscribing data")
#     # print(type(data))
    
#     jsonobj=json.dumps(data)
#     # print(type(jsonobj))
#     #print(jsonobj)
#     res=json.loads(jsonobj)['status']
#     info = json.loads(res)
#     print(info['appsetting']['DB_Name'])
#     dbfile=info['appsetting']['DB_Name']
#     print("Done")
#     ClearAllTables(dbfile)
#     UpdateAllTables(dbfile,info)
#     print("Done")

#     #NCS_Trends_Data_Handler(data)
#     #sensor_Data_Handler(data)



# def on_subscribe(mosq, obj, mid, granted_qos):
#     pass

# mqttc = mqtt.Client()
# mqttc.username_pw_set(mqtt_username, mqtt_password)
# # Assign event callbacks
# mqttc.on_message = on_message
# mqttc.on_connect = on_connect
# mqttc.on_subscribe = on_subscribe


# # Connect
# mqttc.connect(mqtt_broker_ip, int(MQTT_Port), int(Keep_Alive_Interval))

# # Continue the network loop
# mqttc.loop_forever()

import paho.mqtt.client as mqtt
import json
import ssl
from getmyip import get_ip
from ToolHandler import *

# MQTT Settings
MQTT_Port = 8883
Keep_Alive_Interval = 45
mqtt_broker_ip = '5ccaf87576e04605a3c0b13e35dd0680.s1.eu.hivemq.cloud'
mqtt_topic = 'Tool/ToolData'
mqtt_username = 'jerish716' 
mqtt_password = 'jerish716'

# Subscribe to all Sensors at Base Topic
print("Connecting...")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe(mqtt_topic)
    else:
        print(f"Connection failed with code {rc}")

# Save Data into DB Table
def on_message(client, userdata, message):
    # This is the Master Call for saving MQTT Data into DB
    # For details of "sensor_Data_Handler" function please refer "sensor_data_to_db.py"
    topictmp, clienttmp = message.topic.split("/", 1)
    data = dict(
        topic=topictmp,
        client=clienttmp,
        status=message.payload.decode()
    )
    print("Subscribing data")
    jsonobj = json.dumps(data)
    res = json.loads(jsonobj)['status']
    info = json.loads(res)
    print(info['appsetting']['DB_Name'])
    dbfile = info['appsetting']['DB_Name']
    print("Done")
    ClearAllTables(dbfile)
    UpdateAllTables(dbfile, info)
    print("Done")

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscribed: {mid} {granted_qos}")

mqttc = mqtt.Client()

# Set the username and password for the broker
mqttc.username_pw_set(mqtt_username, mqtt_password)

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Configure TLS/SSL
mqttc.tls_set(tls_version=ssl.PROTOCOL_TLS)

try:
    # Connect to the broker
    mqttc.connect(mqtt_broker_ip, MQTT_Port, Keep_Alive_Interval)
    
    # Continue the network loop
    mqttc.loop_forever()
except Exception as e:
    print(f"Connection failed: {e}")

