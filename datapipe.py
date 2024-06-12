#------------------------------------------
#--- Author: Pradeep Singh
#--- Date: 20th January 2017
#--- Version: 1.0
#--- Python Ver: 2.7
#--- Details At: https://iotbytes.wordpress.com/store-mqtt-data-from-sensors-into-sql-database/
#------------------------------------------


import json
import sqlite3
import datetime
from user import *

# SQLite DB Name
#DB_Name =  "IoT.db"

#===============================================================
# Database Manager Class

class DatabaseManager():
	def __init__(self):
		#self.conn = sqlite3.connect(DB_Name)
		try:
			conn = sqlite3.connect(DB_Name)
		except Error as e:
			print(e)
		self.conn._open_connection()
		self.conn.execute('pragma foreign_keys = on')
		self.conn.commit()
		self.cur = self.conn.cursor()
		

		# print("here")
		# cur.execute('''SELECT SwitchID, Date_n_Time, Status FROM NCS_Trends_Data''')
		# all_rows = cur.fetchall()
		# for row in all_rows:
		# 	print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))
		# return

	def DestroyConnection(self):
		self.cur.close()
		self.conn.close()

#===============================================================
# Functions to push Sensor Data into Database
def NCS_Trends_Data_Handler(Data_modified):
	SwitchID = Data_modified['client']
	Data_and_Time = Data_modified['Date']
	Status = Data_modified['status']
	try:
		db = sqlite3.connect(DB_Name)

		cursor = db.cursor()
		db.execute('''INSERT INTO NCSHistory (SwitchID, Date_n_Time, Status) VALUES(?,?,?)''', (SwitchID,Data_and_Time, Status))
		db.commit()
	except Exception as e:
		print(e)
    #db.rollback()
    #raise e
	finally:
		db.close()
	print ("Inserted NCS Data into Database.")
#===============================================================
# Master Function to Select DB Funtion based on MQTT Topic
numberseries = 0
dsptxt = ["some_value", "0", "another_value"]
def sensor_Data_Handler(Data):
	if int(numberseries)==0 and dsptxt[1] != "0" :
		Data['client']=dsptxt[int(Data['client'])]
	elif int(numberseries)!=0 and dsptxt[1]=="0":
		Data['client']=numberseries*Data['client']
	if Data['status']=="150":
		Data['status']="ON"
	elif Data['status']=="180":
		Data['status']="OFF"
	Data['Date']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	NCS_Trends_Data_Handler(Data)

