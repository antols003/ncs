# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 16:21:44 2020

@author: Desk-12
"""

import sqlite3
import os
dbfile='datafarm.db'

def createProjectDetailsTable(Fields,ProjData):
    dbase = sqlite3.connect('datafarm1.db',timeout=1) 
    cursor = dbase.cursor()
    cursor.execute("DROP TABLE IF EXISTS ProjectDetails")
    cursor.execute('''CREATE TABLE IF NOT EXISTS ProjectDetails(
        ID INT PRIMARY KEY NOT NULL,
        PARAMETER TEXT NOT NULL,
        VALUE TEXT NOT NULL)''')
    for i in range(0,len(Fields)):
        cursor.execute("INSERT INTO ProjectDetails(ID,PARAMETER,VALUE) values(?,?,?)",(i+1,Fields[i],ProjData[i]))
        dbase.commit()
    dbase.close()


def bedcount(func,val=None):
    dbase = sqlite3.connect('datafarm1.db',timeout=1) 
    cursor = dbase.cursor()
    if func=="FETCH":
        cursor.execute('''SELECT VALUE FROM ProjectDetails WHERE PARAMETER="Total Beds"''')
        bedsC = cursor.fetchone()
        print(bedsC[0])
        dbase.close()
        return int(bedsC[0])
    if func=="UPDATE":
        cursor.execute("UPDATE ProjectDetails SET VALUE = "+str(val)+" WHERE PARAMETER = 'Total Beds'")
        dbase.commit()
    dbase.close()
    
def getlastcount(tablename):
    dbase = sqlite3.connect('datafarm1.db',timeout=1) 
    cursor = dbase.cursor()
    cursor.execute("SELECT COUNT(ID) FROM "+tablename)
    data=cursor.fetchone()
    dbase.close()
    return data[0]

def createbrstmapping(dbfile):
    try:
        dbase = sqlite3.connect(dbfile,timeout=1) 
        cursor = dbase.cursor()
        cursor.execute("DROP TABLE IF EXISTS brstmapping")
        cursor.execute('''CREATE TABLE brstmapping (
            id integer primary key autoincrement,
            deviceid integer,
            bedname text,
            restroomname text,
            doorlightname text,
            unique (deviceid,bedname, restroomname,doorlightname)
            )''')
        dbase.close()
    except Exception as e:
        print(e)

def insertbrstmapping(dbfile,details):
    dbase = sqlite3.connect(dbfile,timeout=1) 
    cursor = dbase.cursor()
    try: 
        cursor.execute("INSERT INTO brstmapping(deviceid,bedname,restroomname,doorlightname) values(?,?,?,?)",(details[0],details[1],details[2],details[3]) )
        dbase.commit()
        dbase.close()
        return True
    except Exception as e:
        print(e)
        dbase.close()
        return False
    
def createbednaming(dbfile):
    try:
        dbase = sqlite3.connect(dbfile,timeout=1) 
        cursor = dbase.cursor()
        cursor.execute("DROP TABLE IF EXISTS bednaming")
        cursor.execute('''CREATE TABLE bednaming (
            id integer primary key autoincrement,
            deviceid integer,
            bedname integer,
            unique (deviceid, bedname)
            )''')
        dbase.close()
    except Exception as e:
        print(e)
    
def insertbednamingdetails(dbfile,details):
    try:
        dbase = sqlite3.connect(dbfile,timeout=1) 
        cursor = dbase.cursor()
        try: 
            cursor.execute("INSERT INTO bednaming(deviceid,bedname) values(?,?)",(details[0],details[1]) )
            dbase.commit()
            dbase.close()
            return True
        except Exception as e:
            print(e)
            dbase.close()
            return False
    except Exception as e:
        print(e)
    
    
def createdoorlightnaming(dbfile):
    try:
        dbase = sqlite3.connect(dbfile,timeout=1) 
        cursor = dbase.cursor()
        cursor.execute("DROP TABLE IF EXISTS doorlightnaming")
        cursor.execute('''CREATE TABLE doorlightnaming (
            id integer primary key autoincrement,
            deviceid text,
            doorlightname text,
            unique (deviceid, doorlightname)
            )''')
        dbase.close()
    except Exception as e:
        print(e)

def insertdoorlightnaming(dbfile,details):
    dbase = sqlite3.connect(dbfile,timeout=1) 
    cursor = dbase.cursor()
    try: 
        cursor.execute("INSERT INTO doorlightnaming(deviceid,doorlightname) values(?,?)",(details[0],details[1]) )
        dbase.commit()
        dbase.close()
        return True
    except Exception as e:
        print(e)
        dbase.close()
        return False
    
    
def createrestroomnaming(dbfile):
    try:
        dbase = sqlite3.connect(dbfile,timeout=1) 
        cursor = dbase.cursor()
        cursor.execute("DROP TABLE IF EXISTS restroomnaming")
        cursor.execute('''CREATE TABLE restroomnaming (
            id integer primary key autoincrement,
            deviceid text,
            restroomname text,
            unique (deviceid, restroomname)
            )''')
        dbase.close()
    except Exception as e:
        print(e)
    
def insertrestroomnaming(dbfile,details):
    dbase = sqlite3.connect(dbfile,timeout=1) 
    cursor = dbase.cursor()
    try: 
        cursor.execute("INSERT INTO restroomnaming(deviceid,restroomname) values(?,?)",(details[0],details[1]) )
        dbase.commit()
        dbase.close()
        return True
    except Exception as e:
        print(e)
        dbase.close()
        return False

def createdevicetobedmapping(dbfile):
    try:
        dbase = sqlite3.connect(dbfile,timeout=1) 
        cursor = dbase.cursor()
        cursor.execute("DROP TABLE IF EXISTS devicetobedmapping")
        cursor.execute('''CREATE TABLE devicetobedmapping (
            id integer primary key autoincrement,
            deviceid integer,
            bedname text,
            boxid integer,
            unique (deviceid, bedname,boxid)
            )''')
        dbase.close()
    except Exception as e:
        print(e)

def insertdevicetobedmapping(dbfile,details):
    dbase = sqlite3.connect(dbfile,timeout=1) 
    cursor = dbase.cursor()
    try: 
        cursor.execute("INSERT INTO devicetobedmapping(deviceid,bedname,boxid) values(?,?,?)",(details[0],details[1],details[2])) 
        dbase.commit()
        dbase.close()
        return True
    except Exception as e:
        print(e)
        dbase.close()
        return False

def createAppSettingTable(dbfile,data):
    try:
        dbase = sqlite3.connect(dbfile,timeout=1) 
        cursor = dbase.cursor()
        cursor.execute("DROP TABLE IF EXISTS appsetting")
        cursor.execute('''CREATE TABLE IF NOT EXISTS appsetting (id integer primary key autoincrement,
        settingname text not null,
        settingvalue text not null,
        unique (settingname)
    )''')
        key=list(data.keys())
        for k in key:
            cursor.execute("INSERT INTO appsetting(id,settingname,settingvalue) values(?,?,?)",(key.index(k)+1,k,data[k]))
            dbase.commit()
            
        dbase.close()
    except Exception as e:
        print(e)

def truncateHistoryTable(dbfile):
    try:
        dbase = sqlite3.connect(dbfile,timeout=1) 
        cursor = dbase.cursor()
        cursor.execute("DELETE FROM NCS_Trans;")
        dbase.commit()
        print("Cleared history")
        dbase.close()
    except Exception as e:
        print(e)

def ClearHistory(dbfile):
    try:
        dbase = sqlite3.connect(dbfile,timeout=1) 
        cursor = dbase.cursor()
        cursor.execute("DROP TABLE IF EXISTS NCSHistory")
        dbase.close()
    except Exception as e:
        print(e)

#c=bedcount("FETCH")  
#bedcount("UPDATE",30)
#c=bedcount("FETCH") 
#createProjectDetailsTable(["a","b",],["1","2"]) 
#c=getlastcount("ProjectDetails")
#print(c)
#createdevicetobedmapping()
#print(insertdevicetobedmapping([14, '501T', 6]))

#print(list(data.values()))

#

#createSQLTables('/var/datafarm.db')   