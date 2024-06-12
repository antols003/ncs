
# import paho.mqtt.client as mqtt
# from datapipe import sensor_Data_Handler
# from user import *
# # MQTT Settings 
# MQTT_Port = 1883
# Keep_Alive_Interval = 45

# #Subscribe to all Sensors at Base Topic
# print ("connected...")
# def on_connect(client, userdata, flags, rc):
# 	mqttc.subscribe(mqtt_topic)
# 	print ("connected...")

# #Save Data into DB Table
# def on_message(client, userdata, message):
# 	# This is the Master Call for saving MQTT Data into DB
# 	# For details of "sensor_Data_Handler" function please refer "sensor_data_to_db.py"
# 	topictmp,clienttmp=message.topic.split("/",1)
# 	data = dict(
#         topic=topictmp,
#         client=clienttmp,
#         #topic=message.topic,
#         status=message.payload.decode()
#         #client=message.clientID
#     )
# 	print (data)
# 	#NCS_Trends_Data_Handler(data)
# 	sensor_Data_Handler(data)

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
from user import mqtt_username, mqtt_password, mqtt_topic, mqtt_broker_ip

# MQTT Settings 
MQTT_Port = 1883
Keep_Alive_Interval = 45

#Subscribe to all Sensors at Base Topic
print("connected...")

def on_connect(client, userdata, flags, rc):
    client.subscribe(mqtt_topic)
    print("connected...")

#Save Data into DB Table
def on_message(client, userdata, message):
    # This is the Master Call for saving MQTT Data into DB
    # For details of "sensor_Data_Handler" function please refer "sensor_data_to_db.py"
    topictmp, clienttmp = message.topic.split("/", 1)
    data = dict(
        topic=topictmp,
        client=clienttmp,
        # topic=message.topic,
        status=message.payload.decode()
        # client=message.clientID
    )
    print(data)
    # NCS_Trends_Data_Handler(data)
    # sensor_Data_Handler(data)

def on_subscribe(mosq, obj, mid, granted_qos):
    pass

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
# Assign event callbacks
client.on_message = on_message
client.on_connect = on_connect
client.on_subscribe = on_subscribe

# Connect
client.connect(mqtt_broker_ip, int(MQTT_Port), int(Keep_Alive_Interval))

# Continue the network loop
client.loop_forever()

