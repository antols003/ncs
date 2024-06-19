# # -*- coding: utf-8 -*-
# """
# Created on Thu Nov 26 16:21:44 2020

# @author: Desk-12
# """

# import sqlite3
# import os
# dbfile='datafarm.db'

# def createProjectDetailsTable(Fields,ProjData):
#     con = None
#     cur = None
#     try:
#         con = sqlite3.connect('datafarm.db',timeout=1) 
#         print("Connected to database successfully")
#         cur = con.cursor()
#         cur.execute("DROP TABLE IF EXISTS ProjectDetails")
#         cur.execute('''CREATE TABLE IF NOT EXISTS ProjectDetails(
#             ID INT PRIMARY KEY NOT NULL,
#             PARAMETER TEXT NOT NULL,
#             VALUE TEXT NOT NULL)''')
#         for i in range(0,len(Fields)):
#             cur.execute("INSERT INTO ProjectDetails(ID,PARAMETER,VALUE) values(?,?,?)",(i+1,Fields[i],ProjData[i]))
#             con.commit()
#     finally:
#         if con:
#             cur.close()
#             con.close()


# def bedcount(func,val=None):
#     con = None
#     cur = None
#     try:
#         con = sqlite3.connect('datafarm.db',timeout=1) 
#         print("db created")
#         cur = con.cursor()
#         if func=="FETCH":
#             cur.execute('''SELECT VALUE FROM ProjectDetails WHERE PARAMETER="Total Beds"''')
#             bedsC = cur.fetchone()
#             print(bedsC[0])
#             return int(bedsC[0])
#         if func=="UPDATE":
#             cur.execute("UPDATE ProjectDetails SET VALUE = "+str(val)+" WHERE PARAMETER = 'Total Beds'")
#             con.commit()
#     finally:
#         if con:
#             cur.close()
#             con.close()
    
# def getlastcount(tablename):
#     con = None
#     cur = None
#     try:
#         con = sqlite3.connect('datafarm.db',timeout=1) 
#         cur = con.cursor()
#         cur.execute("SELECT COUNT(ID) FROM "+tablename)
#         data=cur.fetchone()
#         return data[0]
#     finally:
#         if con:
#             cur.close()
#             con.close()

# def createbrstmapping(dbfile):
#     con = None
#     cur = None
#     try:
#         con = sqlite3.connect(dbfile,timeout=1) 
#         cur = con.cursor()
#         cur.execute("DROP TABLE IF EXISTS brstmapping")
#         cur.execute('''CREATE TABLE brstmapping (
#             id integer primary key autoincrement,
#             deviceid integer,
#             bedname text,
#             restroomname text,
#             doorlightname text,
#             unique (deviceid,bedname, restroomname,doorlightname)
#             )''')
#     except Exception as e:
#         print(e)
#     finally:
#         if con:
#             cur.close()
#             con.close()

# def insertbrstmapping(dbfile,details):
#     con = None
#     cur = None
    
#     try: 
#         con = sqlite3.connect(dbfile,timeout=1) 
#         cur = con.cursor()
#         cur.execute("INSERT INTO brstmapping(deviceid,bedname,restroomname,doorlightname) values(?,?,?,?)",(details[0],details[1],details[2],details[3]) )
#         con.commit()
#         return True
#     except Exception as e:
#         print(e)
#         return False
#     finally:
#         if con:
#             cur.close()
#             con.close()
    
# def createbednaming(dbfile):
#     con = None
#     cur = None
#     try:
#         con = sqlite3.connect(dbfile,timeout=1) 
#         cur = con.cursor()
#         cur.execute("DROP TABLE IF EXISTS bednaming")
#         cur.execute('''CREATE TABLE bednaming (
#             id integer primary key autoincrement,
#             deviceid integer,
#             bedname integer,
#             unique (deviceid, bedname)
#             )''')
#     except Exception as e:
#         print(e)
#     finally:
#         if con:
#             cur.close()
#             con.close()
    
# def insertbednamingdetails(dbfile,details):
#     con = None
#     cur = None
#     try:
#         con = sqlite3.connect(dbfile,timeout=1) 
#         cur = con.cursor()
#         try: 
#             cur.execute("INSERT INTO bednaming(deviceid,bedname) values(?,?)",(details[0],details[1]) )
#             con.commit()
#             return True
#         except Exception as e:
#             print(e)
#             return False
#     except Exception as e:
#         print(e)
#     finally:
#         if con:
#             cur.close()
#             con.close()
    
    
# def createdoorlightnaming(dbfile):
#     con = None
#     cur = None
#     try:
#         con = sqlite3.connect(dbfile,timeout=1) 
#         cur = con.cursor()
#         cur.execute("DROP TABLE IF EXISTS doorlightnaming")
#         cur.execute('''CREATE TABLE doorlightnaming (
#             id integer primary key autoincrement,
#             deviceid text,
#             doorlightname text,
#             unique (deviceid, doorlightname)
#             )''')

#     except Exception as e:
#         print(e)
#     finally:
#         if con:
#             cur.close()
#             con.close()

# def insertdoorlightnaming(dbfile,details):
#     con = None
#     cur = None
#     con = sqlite3.connect(dbfile,timeout=1) 
#     cur = con.cursor()
#     try: 
#         cur.execute("INSERT INTO doorlightnaming(deviceid,doorlightname) values(?,?)",(details[0],details[1]) )
#         con.commit()
#         return True
#     except Exception as e:
#         print(e)

#         return False
#     finally:
#         if con:
#             cur.close()
#             con.close()
    
# def createrestroomnaming(dbfile):
#     con = None
#     cur = None
#     try:
#         con = sqlite3.connect(dbfile,timeout=1) 
#         cur = con.cursor()
#         cur.execute("DROP TABLE IF EXISTS restroomnaming")
#         cur.execute('''CREATE TABLE restroomnaming (
#             id integer primary key autoincrement,
#             deviceid text,
#             restroomname text,
#             unique (deviceid, restroomname)
#             )''')
#     except Exception as e:
#         print(e)
#     finally:
#         if con:
#             cur.close()
#             con.close()

# def insertrestroomnaming(dbfile,details):
#     con = None
#     cur = None   
#     try:
#         con = sqlite3.connect(dbfile,timeout=1) 
#         cur = con.cursor() 
#         cur.execute("INSERT INTO restroomnaming(deviceid,restroomname) values(?,?)",(details[0],details[1]) )
#         con.commit()
#         return True
#     except Exception as e:
#         print(e)

#         return False
#     finally:
#         if con:
#             cur.close()
#             con.close()

# def createdevicetobedmapping(dbfile):
#     con = None
#     cur = None
#     try:
#         con = sqlite3.connect(dbfile,timeout=1) 
#         cur = con.cursor()
#         cur.execute("DROP TABLE IF EXISTS devicetobedmapping")
#         cur.execute('''CREATE TABLE devicetobedmapping (
#             id integer primary key autoincrement,
#             deviceid integer,
#             bedname text,
#             boxid integer,
#             unique (deviceid, bedname,boxid)
#             )''')
#     except Exception as e:
#         print(e)
#     finally:
#         if con:
#             cur.close()
#             con.close()

# def insertdevicetobedmapping(dbfile,details):
#     con = None
#     cur = None
    
#     try: 
#         con = sqlite3.connect(dbfile,timeout=1) 
#         cur = con.cursor()
#         cur.execute("INSERT INTO devicetobedmapping(deviceid,bedname,boxid) values(?,?,?)",(details[0],details[1],details[2])) 
#         con.commit()
#         return True
#     except Exception as e:
#         print(e)
#         return False
#     finally:
#         if con:
#             cur.close()
#             con.close()

# def createAppSettingTable(dbfile,data):
#     con = None
#     cur = None
#     try:
#         con = sqlite3.connect(dbfile,timeout=1) 
#         cur = con.cursor()
#         cur.execute("DROP TABLE IF EXISTS appsetting")
#         cur.execute('''CREATE TABLE IF NOT EXISTS appsetting (id integer primary key autoincrement,
#         settingname text not null,
#         settingvalue text not null,
#         unique (settingname)
#     )''')
#         print("App Setting--")
#         key=list(data.keys())
#         for k in key:
#             cur.execute("INSERT INTO appsetting(id,settingname,settingvalue) values(?,?,?)",(key.index(k)+1,k,data[k]))
#             con.commit()

#             print(k,data[k])

#     except Exception as e:
#         print(e)
#     finally:
#         if con:
#             cur.close()
#             con.close()

# def truncateHistoryTable(dbfile):
#     con = None
#     cur = None
#     try:
#         con = sqlite3.connect(dbfile,timeout=1) 
#         cur = con.cursor()
#         cur.execute("DELETE FROM NCS_Trans;")
#         con.commit()
#         print("Cleared history")

#     except Exception as e:
#         print(e)
#     finally:
#         if con:
#             cur.close()
#             con.close()

# def ClearHistory(dbfile):
#     con = None
#     cur = None
#     try:
#         con = sqlite3.connect(dbfile,timeout=1) 
#         cur = con.cursor()
#         cur.execute("DROP TABLE IF EXISTS NCSHistory")

#     except Exception as e:
#         print(e)
#     finally:
#         if con:
#             cur.close()
#             con.close()

# def ClearAllTables(dbfile):
#     con = None
#     cur = None
#     try:
#         con = sqlite3.connect(dbfile,timeout=1) 
#         cur = con.cursor()
#         tables=["NCS_Trans","NCSHistory","appsetting","devicetobedmapping","restroomnaming","bednaming","brstmapping"]
#         for tab in tables:
#             cur.execute("DELETE FROM "+tab)
#             cur.execute("UPDATE sqlite_sequence  SET seq = ? where name=?", (0,tab))    
#         con.commit()
#         print("Cleared history")

#     except Exception as e:
#         print(e)
#     finally:
#         if con:
#             cur.close()
#             con.close()

# def UpdateAllTables(dbfile,Alldata):
#     print(Alldata['bedmapping'])
    
#     for data in Alldata['bedmapping']:
#         print('bed',data)
#         insertbednamingdetails(dbfile,data)

#     for data in Alldata['restroomnaming']:
#         print('restroom',data)
#         insertrestroomnaming(dbfile,data)
        
#     for data in Alldata['doorlightnaming']:
#         print('DoorLight',data)
#         insertdoorlightnaming(dbfile,data)

#     for data in Alldata['devicetobedmapping']:
#         print('DeviceToBed',data)
#         insertdevicetobedmapping(dbfile,data)
#     brstdata=Alldata['brstmapping'] 
#     createAppSettingTable(dbfile,Alldata['appsetting'])
#     os.system("sudo hwclock --set --date '"+Alldata['DateTime']+"'")
#     try:  
#         for data in brstdata:
#             beds=brstdata[data]["Bed"]
#             devIds=brstdata[data]["DevID"]
#             for i in range(0,len(beds)):
#                 details=devIds[i],beds[i],brstdata[data]['Toilet'],brstdata[data]['DoorLight']
#                 print("Mapping..",data)
#                 insertbrstmapping(dbfile,details)
        
#     except Exception as e:
#         print(e)
# # -----------------------------------------------------------------------------------

import sqlite3
import os

dbfile = 'datafarm.db'

def create_all_tables():
    con = sqlite3.connect(dbfile, timeout=1)
    cur = con.cursor()
    
    cur.execute("DROP TABLE IF EXISTS ProjectDetails")
    cur.execute('''CREATE TABLE IF NOT EXISTS ProjectDetails(
        ID INT PRIMARY KEY NOT NULL,
        PARAMETER TEXT NOT NULL,
        VALUE TEXT NOT NULL)''')

    cur.execute("DROP TABLE IF EXISTS brstmapping")
    cur.execute('''CREATE TABLE brstmapping (
        id integer primary key autoincrement,
        deviceid integer,
        bedname text,
        restroomname text,
        doorlightname text,
        unique (deviceid, bedname, restroomname, doorlightname)
        )''')
    
    cur.execute("DROP TABLE IF EXISTS bednaming")
    cur.execute('''CREATE TABLE bednaming (
        id integer primary key autoincrement,
        deviceid integer,
        bedname integer,
        unique (deviceid, bedname)
        )''')
    
    cur.execute("DROP TABLE IF EXISTS doorlightnaming")
    cur.execute('''CREATE TABLE doorlightnaming (
        id integer primary key autoincrement,
        deviceid text,
        doorlightname text,
        unique (deviceid, doorlightname)
        )''')
    
    cur.execute("DROP TABLE IF EXISTS restroomnaming")
    cur.execute('''CREATE TABLE restroomnaming (
        id integer primary key autoincrement,
        deviceid text,
        restroomname text,
        unique (deviceid, restroomname)
        )''')
    
    cur.execute("DROP TABLE IF EXISTS devicetobedmapping")
    cur.execute('''CREATE TABLE devicetobedmapping (
        id integer primary key autoincrement,
        deviceid integer,
        bedname text,
        boxid integer,
        unique (deviceid, bedname, boxid)
        )''')
    
    cur.execute("DROP TABLE IF EXISTS appsetting")
    cur.execute('''CREATE TABLE IF NOT EXISTS appsetting (
        id integer primary key autoincrement,
        settingname text not null,
        settingvalue text not null,
        unique (settingname)
        )''')
    
    con.commit()
    cur.close()
    con.close()
    print("All tables created successfully")

def insert_initial_data():
    con = sqlite3.connect(dbfile, timeout=1)
    cur = con.cursor()
    
    fields = ["Total Beds", "Hospital Name"]
    proj_data = ["100", "City Hospital"]
    for i in range(len(fields)):
        cur.execute("INSERT INTO ProjectDetails(ID, PARAMETER, VALUE) values(?,?,?)", (i+1, fields[i], proj_data[i]))
    
    brst_details = [1, "Bed1", "Restroom1", "DoorLight1"]
    cur.execute("INSERT INTO brstmapping(deviceid, bedname, restroomname, doorlightname) values(?,?,?,?)", (brst_details[0], brst_details[1], brst_details[2], brst_details[3]))
    
    bed_details = [1, "Bed1"]
    cur.execute("INSERT INTO bednaming(deviceid, bedname) values(?,?)", (bed_details[0], bed_details[1]))
    
    doorlight_details = ["Device1", "DoorLight1"]
    cur.execute("INSERT INTO doorlightnaming(deviceid, doorlightname) values(?,?)", (doorlight_details[0], doorlight_details[1]))
    
    restroom_details = ["Device1", "Restroom1"]
    cur.execute("INSERT INTO restroomnaming(deviceid, restroomname) values(?,?)", (restroom_details[0], restroom_details[1]))
    
    devicetobed_details = [1, "Bed1", 101]
    cur.execute("INSERT INTO devicetobedmapping(deviceid, bedname, boxid) values(?,?,?)", (devicetobed_details[0], devicetobed_details[1], devicetobed_details[2]))
    
    appsetting_data = {"Setting1": "Value1", "Setting2": "Value2"}
    for key in appsetting_data.keys():
        cur.execute("INSERT INTO appsetting(settingname, settingvalue) values(?,?)", (key, appsetting_data[key]))
    
    con.commit()
    cur.close()
    con.close()
    print("Initial data inserted successfully")

def verify_table_contents(tablename):
    con = sqlite3.connect(dbfile, timeout=1)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM {tablename}")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    con.close()

def ClearAllTables(dbfile):
    con = None
    cur = None
    try:
        con = sqlite3.connect(dbfile, timeout=1) 
        cur = con.cursor()
        tables = ["NCS_Trans", "NCSHistory", "appsetting", "devicetobedmapping", "restroomnaming", "bednaming", "brstmapping"]
        for tab in tables:
            cur.execute("DELETE FROM " + tab)
            cur.execute("UPDATE sqlite_sequence SET seq = ? where name=?", (0, tab))    
        con.commit()
        print("Cleared history")
    except Exception as e:
        print(e)
    finally:
        if con:
            cur.close()
            con.close()

def insertbednamingdetails(dbfile, details):
    con = None
    cur = None
    try:
        con = sqlite3.connect(dbfile, timeout=1)
        cur = con.cursor()
        cur.execute("INSERT INTO bednaming(deviceid, bedname) values(?,?)", (details[0], details[1]))
        con.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        if con:
            cur.close()
            con.close()

def insertrestroomnaming(dbfile, details):
    con = None
    cur = None   
    try:
        con = sqlite3.connect(dbfile, timeout=1)
        cur = con.cursor()
        cur.execute("INSERT INTO restroomnaming(deviceid, restroomname) values(?,?)", (details[0], details[1]))
        con.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        if con:
            cur.close()
            con.close()

def insertdoorlightnaming(dbfile, details):
    con = None
    cur = None
    try:
        con = sqlite3.connect(dbfile, timeout=1)
        cur = con.cursor()
        cur.execute("INSERT INTO doorlightnaming(deviceid, doorlightname) values(?,?)", (details[0], details[1]))
        con.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        if con:
            cur.close()
            con.close()

def insertdevicetobedmapping(dbfile, details):
    con = None
    cur = None
    try:
        con = sqlite3.connect(dbfile, timeout=1)
        cur = con.cursor()
        cur.execute("INSERT INTO devicetobedmapping(deviceid, bedname, boxid) values(?,?,?)", (details[0], details[1], details[2]))
        con.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        if con:
            cur.close()
            con.close()

def insertbrstmapping(dbfile, details):
    con = None
    cur = None
    try: 
        con = sqlite3.connect(dbfile, timeout=1)
        cur = con.cursor()
        cur.execute("INSERT INTO brstmapping(deviceid, bedname, restroomname, doorlightname) values(?,?,?,?)", (details[0], details[1], details[2], details[3]))
        con.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        if con:
            cur.close()
            con.close()

def createAppSettingTable(dbfile, data):
    con = None
    cur = None
    try:
        con = sqlite3.connect(dbfile, timeout=1)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS appsetting")
        cur.execute('''CREATE TABLE IF NOT EXISTS appsetting (
            id integer primary key autoincrement,
            settingname text not null,
            settingvalue text not null,
            unique (settingname)
            )''')
        print("App Setting--")
        for key, value in data.items():
            cur.execute("INSERT INTO appsetting(settingname, settingvalue) values(?,?)", (key, value))
        con.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        if con:
            cur.close()
            con.close()

def UpdateAllTables(dbfile, Alldata):
    print(Alldata['bedmapping'])
    
    for data in Alldata['bedmapping']:
        print('bed',data)
        insertbednamingdetails(dbfile,data)

    for data in Alldata['restroomnaming']:
        print('restroom',data)
        insertrestroomnaming(dbfile,data)
        
    for data in Alldata['doorlightnaming']:
        print('DoorLight',data)
        insertdoorlightnaming(dbfile,data)

    for data in Alldata['devicetobedmapping']:
        print('DeviceToBed',data)
        insertdevicetobedmapping(dbfile,data)
    brstdata=Alldata['brstmapping'] 
    createAppSettingTable(dbfile,Alldata['appsetting'])
    os.system("sudo hwclock --set --date '"+Alldata['DateTime']+"'")
    try:  
        for data in brstdata:
            beds=brstdata[data]["Bed"]
            devIds=brstdata[data]["DevID"]
            for i in range(0,len(beds)):
                details=devIds[i],beds[i],brstdata[data]['Toilet'],brstdata[data]['DoorLight']
                print("Mapping..",data)
                insertbrstmapping(dbfile,details)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    create_all_tables()
    insert_initial_data()
    
    # Verify contents of the tables
    tables = ['ProjectDetails', 'brstmapping', 'bednaming', 'doorlightnaming', 'restroomnaming', 'devicetobedmapping', 'appsetting']
    for table in tables:
        print(f"Contents of {table}:")
        verify_table_contents(table)
    
    # Example data for UpdateAllTables
    info = {
        'bedmapping': [[1, 'Bed1']],
        'restroomnaming': [['Device1', 'Restroom1']],
        'doorlightnaming': [['Device1', 'DoorLight1']],
        'devicetobedmapping': [[1, 'Bed1', 101]],
        'brstmapping': {
            'ExampleData': {
                'Bed': ['Bed1'],
                'DevID': [1],
                'Toilet': 'Restroom1',
                'DoorLight': 'DoorLight1'
            }
        },
        'appsetting': {'Setting1': 'Value1', 'Setting2': 'Value2'},
        'DateTime': '2023-06-09 12:34:56'
    }

    ClearAllTables(dbfile)
    UpdateAllTables(dbfile, info)
    
    # Verify contents of the tables after updates
    for table in tables:
        print(f"Contents of {table} after updates:")
        verify_table_contents(table)
