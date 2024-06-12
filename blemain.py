		
#!/usr/bin/env python
import os
from bluetooth import *
from wifi import Cell, Scheme
import subprocess
import time
import BtAutoPair
import bluetooth , subprocess
from dbhandler import *
import dbhandler as dbhandler
wififile= "/etc/wpa_supplicant/wpa_supplicant.conf"
sudo_mode = "sudo"
def chomp(x):
	x=x[:-4]
	return x
def first2(s):
	return s[:2]
def getaudiooutput():
	cmd="amixer cget numid=3 | grep ': values'| awk -F '=' '{print $2}'"
	cmd_result = ""
	cmd_result=subprocess.check_output(cmd , shell=True)
	cmd_result=str(cmd_result.decode("utf-8"))
	cmd_result=cmd_result[:-1]
	return cmd_result
def getvolumelevel():
	cmd="amixer -M sget PCM | grep 'Mono:' | awk -F'[][]' '{print $2}'"
	cmd_result = ""
	#cmd_result = os.system(sudo_mode + cmd)
	cmd_result=subprocess.check_output(cmd , shell=True)
	cmd_result=str(cmd_result.decode("utf-8"))
	cmd_result=cmd_result[:-2]
	print(cmd_result)
	return cmd_result
def updateaudiooutput(xdata):
	if(xdata=="hdmi"):
		cmd ="amixer cset numid=3 2"
		cmd_result = ""
		cmd_result = os.system(sudo_mode + cmd)
	elif (xdata=="jack"):
		cmd ="amixer cset numid=3 1"
		cmd_result = ""
		cmd_result = os.system(sudo_mode + cmd)
	return "audiooutputupdated"
def updatevolume(xdata):
	cmd="amixer -q -M sset PCM "+str(xdata)+"%"
	cmd_result = ""
	cmd_result = os.system(sudo_mode + cmd)
	return "volumelevelupdated"
def updatezoom(xdata):
	setsetting("pagezoom",xdata)
	return "zoomupdated"
def updateserverdata(xbat1,xbat2,xbat3):
	setsetting("mqtt_username",xbat1)
	setsetting("mqtt_password",xbat2)
	setsetting("TDU01/#",xbat3)
	data= "serverdataupdated"
	return data
def getserverdata():

	data= readsetting("mqtt_broker_ip")+" "+readsetting("mqtt_username")+" "+readsetting("mqtt_password")+" "+readsetting("mqtt_topic").replace('#', '')
	print(data)
	return data
def updatedipaddress(xdata1,xdata2):
	wififile= "/etc/dhcpcd.conf"
	#sed -i 's/Totale_Doctor_Count=.*/Totale_Doctor_Count=10/' wpa.txt
	cmd ="sed -i \'s/static ip_address=.*/static ip_address="+str(xdata1)+"/\' "+wififile
	cmd_result = ""
	cmd_result = os.system(sudo_mode + cmd)
	cmd ="sed -i \'s/static routers=.*/static routers="+str(xdata2)+"/\' "+wififile
	cmd_result = ""
	cmd_result = os.system(sudo_mode + cmd)
	cmd ="sed -i \'s/static domain_name_servers=.*/static domain_name_servers="+str(xdata2)+"/\' "+wififile
	cmd_result = ""
	cmd_result = os.system(sudo_mode + cmd)
	cmd="dos2unix "+wififile
	cmd_result = ""
	cmd_result = os.system(sudo_mode + cmd)
	setsetting("mqtt_broker_ip",xdata1)
	return "ipaddressupdated"
def updatedocount(xdata):
	setsetting("Que",xdata)
	return "doccountupdated"
def updatewifi(ssid, psk):
	cmd='sed -i  \'/network/,$d\' '+wififile
	cmd_result = os.system(sudo_mode + cmd)
	cmd = ' wpa_passphrase {ssid} {psk} | sudo tee -a {conf} > /dev/null'.format(
			ssid=str(ssid).replace('!', '\!'),
			psk=str(psk).replace('!', '\!'),
			conf=wififile
		)
	cmd_result = ""
	cmd_result = os.system(sudo_mode + cmd)

	# reconfigure wifi
	#cmd = sudo_mode + 'wpa_cli -i wlan0 reconfigure'
	#cmd_result = os.system(cmd)
	return "wifiupdated"
def factoryreset():
	deldatafromtables("doctordetails")
	for i in range(1,51):
		nameis="Doctor-"+str(i)
		readytable(nameis,i)
	deldatafromtables("appsetting")
	intialseetingsetup("Que","5")
	intialseetingsetup("pagezoom","1")
	intialseetingsetup("DB_Name","/var/datafarm.db")
	intialseetingsetup("mqtt_topic","TDU01/#")
	intialseetingsetup("mqtt_password","oora")
	intialseetingsetup("mqtt_username","oora")
	intialseetingsetup("mqtt_broker_ip","192.168.31.230")
	intialseetingsetup("lang","kannada")
	updateaudiooutput("jack")
	updatevolume("100")
	updatedipaddress("192.168.31.230","192.168.31.1")
	return "factoryresetupdated"
def rebootserver():
	cmd="reboot"
	cmd_result = ""
	cmd_result = os.system(sudo_mode + cmd)
def shutdownserver():
	cmd="shutdown now"
	cmd_result = ""
	cmd_result = os.system(sudo_mode + cmd)
def getwifidata():
	datapack={}
	look_for1 = "ssid"
	look_for2 = "psk"
	temp = []
	with open(wififile, "r") as file_to_read:
		for line in file_to_read:
			if look_for1 in line:
				temp.append(line)
	temp=str(temp)
	tempdata=temp.split("\"",2)
	print(tempdata[1] + " -extrateddata[1]")
	datapack[0]= tempdata[1]
	temp = []
	tempdata=0
	with open(wififile, "r") as file_to_read:
		for line in file_to_read:
			if look_for2 in line:
				temp.append(line)
	temp=str(temp)
	tempdata=temp.split("\"",2)
	print(tempdata[1] + " -extrateddata[1]")
	datapack[1]=tempdata[1]
	data= "wifi"+" "+datapack[0] +" "+datapack[1]
	return data
def getstaticipdata():
	datapack={}
	wififile= "/etc/dhcpcd.conf"
	look_for1 = "static ip_address"
	look_for2 = "static routers"
	look_for3 = "static domain_name_servers"
	temp = []
	with open(wififile, "r") as file_to_read:
		for line in file_to_read:
			if look_for1 in line:
				temp.append(line.strip())
	temp=str(temp[0])
	tempdata=temp.split("=",2)
	print(tempdata[1] + " -extrateddata[1]")
	datapack[0]= tempdata[1]

	temp = []
	tempdata=0
	with open(wififile, "r") as file_to_read:
		for line in file_to_read:
			if look_for2 in line:
				temp.append(line.strip())
	temp=str(temp[0])
	tempdata=temp.split("=",2)
	print(tempdata[1] + " -extrateddata[1]")
	datapack[1]=tempdata[1]

	temp = []
	tempdata=0
	with open(wififile, "r") as file_to_read:
		for line in file_to_read:
			if look_for3 in line:
				temp.append(line.strip())
	temp=str(temp[0])
	tempdata=temp.split("=",2)
	print(tempdata[1] + " -extrateddata[1]")
	#datapack[2]=tempdata[1]
	datapack[2]= tempdata[1]
	data= "ip"+" "+datapack[0] +" "+datapack[1]+" "+datapack[2]
	return data
autopair = BtAutoPair.BtAutoPair()
autopair.enable_pairing()
#subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
#subprocess.call(['sudo', 'hciconfig', 'hci0', 'sspmode','1'])
subprocess.call(['sudo', 'sdptool', 'add', 'SP'])


try:
	while True:
		# start the Bluetooth service
		server_sock = BluetoothSocket(RFCOMM)
		server_sock.bind(("", PORT_ANY))
		server_sock.listen(1)
		port = server_sock.getsockname()[1]
		uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

		advertise_service( server_sock, "blackbox",
						   service_id = uuid,
						   service_classes = [uuid, SERIAL_PORT_CLASS],
						   profiles = [SERIAL_PORT_PROFILE] )
						   
		# signal server startup


		# wait for connection
		client_sock, client_info = server_sock.accept()

		# signal successful connection

		try:
			partial = ''
			while True:
				data = client_sock.recv(1024)
				print ("received [%s]" % data)
				if len(data)>0:
					datacleaned=str(data.decode("utf-8"))
					print("datacleaned")
					print(datacleaned)
					if first2(datacleaned)=="$$":
						#print("its a list")
						recevicedata=datacleaned.split('/')
						if recevicedata[1]=="updatewifi":
							client_sock.send(updatewifi(recevicedata[2],recevicedata[3]))
						elif recevicedata[1]=="updatedoccount":
							client_sock.send(updatedocount(str(recevicedata[2])))
						elif recevicedata[1]=="updateipaddress":
							client_sock.send(updatedipaddress(recevicedata[2],recevicedata[3]))
						elif recevicedata[1]=="updatezoom":
							client_sock.send(updatezoom(recevicedata[2]))
						elif recevicedata[1]=="updatevolumelevel":
							client_sock.send(updatevolume(recevicedata[2]))
						elif recevicedata[1]=="updateaudiooutput":
							client_sock.send(updateaudiooutput(recevicedata[2]))


					else:
						if  datacleaned=="currentwifi":
							client_sock.send(getwifidata() )
						elif datacleaned=="staticip":
							client_sock.send(getstaticipdata() )
						elif datacleaned=="wifiandip":
							client_sock.send("wifiandip"+" "+getwifidata()+" "+getstaticipdata() )
						elif datacleaned=="currentdoccount":
							#print(Totale_Doctor_Count)
							client_sock.send("doccount"+" "+readsetting('Que'))
						elif datacleaned=="currentserverdata":
							client_sock.send("serverdata"+" "+getserverdata())
						elif datacleaned=="currentserverdatainit":
							client_sock.send("serverdatainit"+" "+getserverdata())
						elif datacleaned=="AVdata":
							print("currentAVdata"+" "+readsetting('Que')+" "+readsetting('pagezoom')+" "+getaudiooutput()+" "+getvolumelevel())
							client_sock.send("currentAVdata"+" "+readsetting('Que')+" "+readsetting('pagezoom')+" "+getaudiooutput()+" "+getvolumelevel())
						elif datacleaned=="currentzoom":
							client_sock.send("zoom"+" "+readsetting('pagezoom'))
						elif datacleaned=="currentvolumelevel":
							client_sock.send("volumelevel"+" "+getvolumelevel())
						elif datacleaned=="currentaudiooutput":
							client_sock.send("audiooutput"+" "+getaudiooutput())
						elif datacleaned=="factoryreset":
							factoryreset()
							client_sock.send("factoryresetupdated")
						elif datacleaned=="rebootserver":
							rebootserver()
						elif datacleaned=="shutdownserver":
							shutdownserver()




		except IOError:
			pass

	# connection lost
		client_sock.close()
		server_sock.close()

except KeyboardInterrupt:
	print ("disconnected")
	client_sock.close()
	server_sock.close()
	print ("all done")



