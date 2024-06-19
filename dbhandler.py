import sqlite3
from sqlite3 import Error
import datetime
import re
DB_Name="datafarm.db"

def insertUser(username,password):
    con = sqlite3.connect(DB_Name)
    cur = con.cursor()
    cur.execute("INSERT INTO Air_usermang (username,password) VALUES (?,?)", (username,password))
    con.commit()
    con.close()

def retrieveUsers(username,password):
    con = sqlite3.connect(DB_Name)
    cur = con.cursor()
    cur.execute("SELECT username, password FROM Air_usermang where username=? and password=?",(username,password))
    users = cur.fetchall()
    con.close()
    return users
numberseries = 0
dsptxt = ["some_value", "0", "another_value"]

def insertstatus(Data):
    if int(numberseries)==0 and dsptxt[1] != "0" :
        Data['client']=dsptxt[int(Data['client'])]
    elif int(numberseries)!=0 and dsptxt[1]=="0":
        Data['client']=numberseries*Data['client']
    if Data['payload']=="150":
        Data['payload']="Called"
    elif Data['payload']=="180":
        Data['payload']="Attended"
    Data['Date']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con = None
    cur = None
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("INSERT INTO Air_Trends_Data (SwitchID, Date_n_Time, Status) VALUES (?,?,?)", (Data['client'],Data['Date'],Data['payload']))
        con.commit()
        print("data inserted")
    finally:
        if con:
            cur.close()
            con.close()

def insertstatusNCS(Datax):
    # if int(numberseries)==0 and dsptxt[1] != "0" :
    #   Data['client']=dsptxt[int(Data['client'])]
    # elif int(numberseries)!=0 and dsptxt[1]=="0":
    #   Data['client']=numberseries*Data['client']
    if Datax['payload']=="150":
        Datax['payload']="Called"
    elif Datax['payload']=="180":
        Datax['payload']="Attended"
    Datax['Date']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print((Datax['boxname'],Datax['Date'],Datax['payload']))
    con = None
    cur = None
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("INSERT INTO NCSHistory (SwitchID, Date_n_Time, Status) VALUES (?,?,?)", (Datax['boxname'],Datax['Date'],Datax['payload']))
        con.commit()
        print("data inserted")
    except Exception:
        pass
    finally:
        if con:
            cur.close()
            con.close()

def sensor_Data_Handler(Data):
    insertstatusNCS(Data)



def insertwaiter(waiterid,dinntables):
    con = None
    cur = None
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("INSERT INTO Air_waiter (waiter_id,dinn_tables) VALUES (?,?)", (waiterid,dinntables))
        con.commit()
        print("inserted data")
    finally:
        if con:
            cur.close()
            con.close()


def truncateHistoryTable():
    con = None
    cur = None
    try:
        con = sqlite3.connect(DB_Name,timeout=1) 
        cur = con.cursor()
        cur.execute("DELETE FROM NCS_Trans;")
        con.commit()
        print("Cleared history")
    except Exception as e:
        print(e)
    finally:
        if con:
            cur.close()
            con.close()

def clearHistoryTable():
    con = None
    cur = None
    try:
        con = sqlite3.connect(DB_Name,timeout=1) 
        cur = con.cursor()
        cur.execute("DELETE FROM NCS_Trans;")
        con.commit()
        print("Cleared history")
    except Exception as e:
        print(e)
    finally:
        if con:
            cur.close()
            con.close()

def deletewaiter(waiterid):
    con = None
    cur = None
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("DELETE FROM Air_waiter  WHERE waiter_id=?",[waiterid] )
        con.commit()
        print("deleted waiter")
    finally:
        if con:
            cur.close()
            con.close()


def retrievewaiter(waiterid):
    con = None
    cur = None
    waiterlistclean=[]
    l=['(',')',',']
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("SELECT dinn_tables FROM Air_waiter where waiter_id=?",[waiterid])
        waiterlist = cur.fetchall()
        waiterlistclean.append(0)
        for tup in waiterlist:
            t = str(tup).replace("('","").replace("',)","")
            waiterlistclean.append(t)
        #waiterlistclean=[ x.replace(y,'')  for x in waiterlist for y in l if y in x ]
    finally:
        if con:
            cur.close()
            con.close()
    return waiterlistclean
    
def wipedbdata():
    con = None
    cur = None
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("DELETE FROM Air_Trends_Data")
        con.commit()
    finally:
        if con:
            cur.close()
            con.close()

def retrievedoctorroomdetailsjson(row_count):
    con = None
    cur = None
    doctorroomlistclean=[]
    cleanlist=[]
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("SELECT doctorname,roomid  FROM doctordetails ORDER BY id ASC LIMIT ?",[row_count])
        doctorroomlistclean = cur.fetchall()
        print("dbfactorystart")
        for row ,x in doctorroomlistclean:
            case = {'Name': row, 'Id': x}
            cleanlist.append(case)
            print(row)
            print(x)
        print("dbfactoryend")
        print(cleanlist)
    finally:
        if con:
            cur.close()
            con.close()
    #return doctorroomlistclean
    return cleanlist
def retrivebednaming():
    con = None
    cur = None
    bedname=[]
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("SELECT deviceid,bedname FROM bednaming ORDER BY deviceid ASC;")
        bedname = cur.fetchall()
        print(dict(bedname))

    finally:
        if con:
            cur.close()
            con.close()
    #return doctorroomlistclean
    return dict(bedname)

def retrivebox(deviceid):
    con = None
    cur = None
    bedname=[]
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("SELECT boxid,bedname FROM devicetobedmapping where deviceid=? ;",[int(deviceid),])
        bedname = cur.fetchall()
        print(bedname)

    finally:
        if con:
            cur.close()
            con.close()
    #return doctorroomlistclean
    return bedname
def retrivedoorlight_tswitch(restroomname):
    con = None
    cur = None
    bedname=[]
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("SELECT doorlightname FROM brstmapping where restroomname=? ;",[restroomname])
        bedname = cur.fetchall()
        print(bedname)

    finally:
        if con:
            cur.close()
            con.close()
    #return doctorroomlistclean
    return bedname


def Switch_IDandCount():
    con = None
    cur = None
    boxData={}
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("SELECT bedname FROM devicetobedmapping;")
        boxnames = cur.fetchall()
        print("BoxNames",boxnames)
        latst_id=0
        for name in boxnames:
            cur.execute("SELECT deviceid,boxid FROM devicetobedmapping where bedname=? ;",[name[0]])
            devId,boxId=cur.fetchall()[0]
            if boxId not in boxData.keys():
                boxData[boxId]=[]
            boxData[boxId].append(devId)
            latst_id=devId

    finally:
        if con:
            cur.close()
            con.close()
    #return doctorroomlistclean
    print("-----",boxData,latst_id)
    return boxData,latst_id

def boxSwitches(boxid):
    con = None
    cur = None
    boxswitches=[]
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("SELECT * FROM devicetobedmapping where boxid=? ;",[boxid])
        boxswitches = cur.fetchall()
        print(boxswitches)

    finally:
        if con:
            cur.close()
            con.close()
    #return doctorroomlistclean
    return len(boxswitches)


def retrivedoorlight_tbed(bedne):
    con = None
    cur = None
    bedname=[]
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("SELECT doorlightname FROM brstmapping where bedname=? ;",[bedne])
        bedname = cur.fetchall()
        print(bedname)

    finally:
        if con:
            cur.close()
            con.close()
    #return doctorroomlistclean
    return bedname

def retrievedoctorroomdetails(row_count):
    con = None
    cur = None
    doctorroomlistclean=[]
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("SELECT doctorname,roomid  FROM doctordetails  ORDER BY id ASC LIMIT ?",[row_count])
        doctorroomlistclean = cur.fetchall()
        for row  in doctorroomlistclean:
            print(row)

    finally:
        if con:
            cur.close()
            con.close()
    return doctorroomlistclean


def retrievedoctor(roomid):
    con = None
    cur = None
    waiterlistclean=[]
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("SELECT doctorname FROM doctordetails where roomid=?",[roomid])
        waiterlist = cur.fetchone()
        catme=waiterlist[0]

    finally:
        if con:
            cur.close()
            con.close()
            print("retrievedoctor")
    return catme


def retrievetokennobydoc(roomid):
    con = None
    cur = None
    waiterlistclean=[]
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("SELECT tokenno FROM doctordetails where roomid=?",[roomid])
        waiterlist = cur.fetchone()
        catme=waiterlist[0]

    finally:
        if con:
            cur.close()
            con.close()
            print("retrieve tokennobydoc")
    return catme


def updatetokennobydoc(roomid,tokenno):
    con = None
    cur = None
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("UPDATE doctordetails  SET tokenno = ? where roomid=?", (tokenno,roomid))
        con.commit()
        print("updated tokennobydoc")
    finally:
        if con:
            cur.close()
            con.close()

def retrievetoken():
    con = None
    cur = None
    waiterlistclean=[]
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("SELECT currenttokenno FROM tokenbank ")
        waiterlist = cur.fetchone()
        catme=waiterlist[0]

    finally:
        if con:
            cur.close()
            con.close()
            print("retrievetokenno")
    return catme

def retrieveissedtoken():
    con = None
    cur = None
    waiterlistclean=[]
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("SELECT issuedtokenno FROM tokenbank ")
        waiterlist = cur.fetchone()
        catme=waiterlist[0]

    finally:
        if con:
            cur.close()
            con.close()
            print("retrievetokenno")
    return catme


def updatetoken(tokenno):
    con = None
    cur = None
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("UPDATE tokenbank  SET currenttokenno = ? ", (tokenno,))
        con.commit()
        print("updated tokenno")
    finally:
        if con:
            cur.close()
            con.close()
def updateissuedtoken(tokenno):
    con = None
    cur = None
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("UPDATE tokenbank  SET issuedtokenno = ? ", (tokenno,))
        con.commit()
        print("updated tokenno")
    finally:
        if con:
            cur.close()
            con.close()

def updatedoctorroomdetails(roomid,docname):
    con = None
    cur = None
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("UPDATE doctordetails  SET doctorname = ? where roomid=?", (docname,roomid))
        con.commit()
        print("updated data")
    finally:
        if con:
            cur.close()
            con.close()


def deldatafromtables(table_name):
    con = None
    cur = None
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        query="DELETE FROM "+table_name+";"
        print(query)
        cur.execute(query)
        con.commit()
        cur.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = ?;" , (table_name,))
        con.commit()
        print("deleted ")
    finally:
        if con:
            cur.close()
            con.close()


def readytable(xname,xid):
    con = None
    cur = None
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("INSERT INTO doctordetails (doctorname,roomid,tokenno) VALUES (?,?,?);", (xname,xid,0,))
        con.commit()
    finally:
        if con:
            cur.close()
            con.close()

def readsetting(appname):
    con = None
    cur = None
    waiterlistclean = []
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        print("App Name:", appname)
        cur.execute("SELECT settingvalue FROM appsetting WHERE settingname = ?;", (appname,))
        waiterlist = cur.fetchone()
        print("SQL Result:", waiterlist)
        if waiterlist is not None:
            catme = waiterlist[0]
            print("Setting Value:", catme)
        else:
            catme = None
            print("Setting Value is None")
    finally:
        if con:
            cur.close()
            con.close()
            print("readapplimit") 
    return catme

def setsetting(appname,ydata):
    con = None
    cur = None
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("UPDATE appsetting  SET settingvalue = ? where settingname=?;", (ydata,appname))
        con.commit()
        #print("setapplimit")
    finally:
        if con:
            cur.close()
            con.close()


def intialseetingsetup(xname,xid):
    con = None
    cur = None
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("INSERT INTO appsetting (settingname,settingvalue) VALUES (?,?);", (xname,xid))
        con.commit()
    finally:
        if con:
            cur.close()
            con.close()


def intialtoken(currnt):
    con = None
    cur = None
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("INSERT INTO tokenbank (currenttokenno,issuedtokenno) VALUES (?,?)", (currnt,currnt,))
        con.commit()
    finally:
        if con:
            cur.close()
            con.close()


def Update_For_Analytics_Noemg(Datax):
    con = None
    cur = None
    NurseStation=readsetting("NurseStation")
    curdate=datetime.datetime.now().strftime("%Y-%m-%d")
    
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("SELECT ID , CallInitiated_Time FROM NCS_Trans  where CallingUnit =? and  Cleared_Time is NULL ",[Datax['boxname']])
        row =cur.fetchone()
        print("select")
        print("row",row)
        if row == None:
            print ("insert")
            if Datax['payload']=="150":
                curtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cur.execute("INSERT INTO NCS_Trans (CallingUnit, myDate, CallInitiated_Time,Nurse_Station) VALUES (?,?,?,?);", (Datax['boxname'],curdate,curtime,NurseStation))
                con.commit()
            elif Datax['payload']=="180":
                pass
        else:
            print("update")
            if Datax['payload']=="150":
                cur.execute("UPDATE NCS_Trans  SET CallInitiated_Time = ?,myDate =?  WHERE ID=?", (curtime,curdate,row[0]))
                con.commit()
            elif Datax['payload']=="180":
                nxtime= datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') 
                curtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                curtimeformated= datetime.datetime.strptime(curtime, '%Y-%m-%d %H:%M:%S') 
                minutes= str(curtimeformated-nxtime)
                cur.execute("UPDATE NCS_Trans  SET Cleared_Time = ?,Duration=? WHERE ID=?", (curtimeformated,minutes,row[0]))
                con.commit()

                
    except Exception:
        pass
        #print(Exception)
    finally:
        if con:
            cur.close()
            con.close()


def Update_For_Analytics(Datax):
    con = None
    cur = None
    emergencySuff=" - Emergency"
    NurseStation=readsetting("NurseStation")
    curdate=datetime.datetime.now().strftime("%Y-%m-%d")
    
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("SELECT ID , CallInitiated_Time FROM NCS_Trans  where CallingUnit =? and  Cleared_Time is NULL ",[Datax['boxname']+emergencySuff])
        row =cur.fetchone()
        cur.execute("SELECT ID , CallInitiated_Time FROM NCS_Trans  where CallingUnit =? and  Cleared_Time is NULL ",[Datax['boxname']])
        row1 =cur.fetchone()
        print("select")
        print("row",row)
        if row == None:
            row=row1
        if row == None:
            print ("insert")
            if Datax['payload']=="150":
                curtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cur.execute("INSERT INTO NCS_Trans (CallingUnit, myDate, CallInitiated_Time,Nurse_Station) VALUES (?,?,?,?);", (Datax['boxname'],curdate,curtime,NurseStation))
                con.commit()
            if Datax['payload']=="210":
                curtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cur.execute("INSERT INTO NCS_Trans (CallingUnit, myDate, CallInitiated_Time,Nurse_Station) VALUES (?,?,?,?);", (Datax['boxname']+emergencySuff,curdate,curtime,NurseStation))
                con.commit()
            elif Datax['payload']=="180":
                pass
        else:
            print("update")
            if Datax['payload']=="150":
                cur.execute("UPDATE NCS_Trans  SET CallInitiated_Time = ?,myDate =?  WHERE ID=?", (curtime,curdate,row[0]))
                con.commit()
            if Datax['payload']=="210":
                cur.execute("UPDATE NCS_Trans  SET CallInitiated_Time = ?,myDate =?  WHERE ID=?", (curtime,curdate,row[0]))
                con.commit()
            elif Datax['payload']=="180":
                nxtime= datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') 
                curtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                curtimeformated= datetime.datetime.strptime(curtime, '%Y-%m-%d %H:%M:%S') 
                minutes= str(curtimeformated-nxtime)

                cur.execute("UPDATE NCS_Trans  SET Cleared_Time = ?,Duration=? WHERE ID=?", (curtimeformated,minutes,row[0]))
                con.commit()

                
    except Exception:
        pass
        #print(Exception)
    finally:
        if con:
            cur.close()
            con.close()

def retrivedatafromDB(dur):
    con = None
    cur = None
    NurseStation=readsetting("NurseStation")
    curdate=datetime.datetime.now().strftime("%Y-%m-%d")
    curtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute('SELECT Nurse_Station , CallingUnit,myDate,CallInitiated_Time,Cleared_Time,Duration,"NO" as Escalation from (SELECT Nurse_Station , CallingUnit,myDate,CallInitiated_Time,Cleared_Time,Duration FROM NCS_Trans where Duration < ?)UNION ALL SELECT Nurse_Station , CallingUnit,myDate,CallInitiated_Time,Cleared_Time,Duration,"YES" as Escalation from (SELECT Nurse_Station , CallingUnit,myDate,CallInitiated_Time,Cleared_Time,Duration FROM NCS_Trans where Duration >?)',(dur,dur))
        row =cur.fetchall()
        #row=row[::-1]
        print("select")
        print("row",row)
        if row != None:
            return row;
        else:
            return 0;
                
    except Exception:
        pass
        #print(Exception)
    finally:
        if con:
            cur.close()
            con.close()

def cleandata():
    con = None
    cur = None
    NurseStation=readsetting("NurseStation")
    curdate=datetime.datetime.now().strftime("%Y-%m-%d")
    curtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        con = sqlite3.connect(DB_Name)
        cur = con.cursor()
        cur.execute("DELETE FROM NCS_Trans WHERE myDate  <= datetime('now','localtime','-183 days');")
        con.commit()
    except Exception:
        pass
        #print(Exception)
    finally:
        if con:
            cur.close()
            con.close() 



#print(retrivedatafromDB("0:03:00"))