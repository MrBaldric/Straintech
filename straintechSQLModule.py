import pymssql, time
from histLogging import errLog

#Translate truck numer in to truck fleet label
def truckNumber(cS, trkNumber):
    dTruckList = {}
    countList = 0
    listLen = len(cS[1])
    while (countList < listLen):
        dTruckList[int(cS[1][countList])] = cS[2][countList]#Build list of Straintech ID's and Fleetnumbers 
        countList += 1
    name = 'null'
    name = dTruckList.get(trkNumber)
    return name


#SQL Queries from straintech fleetmanger database
def sqlConn(sD,fD,cS,tL):
    conn = pymssql.connect(cS[0][0] + "\SQLEXPRESS",cS[0][1],cS[0][2],cS[0][3])
    cur = conn.cursor()
    returnData = []
    errLog("Fetch SQL Data for{}".format(truckNumber(cS, int(tL))))
    cur.execute("select * from dbo.EventData where iEventID = -1 and dtStart > '" + sD + "' and dtStart < '" + fD + "' and iVehicleID = '" + str(tL) + "'")
    time.sleep(0.2)
    row = cur.fetchone()
    if (row == None):
        row = [None,int(tL),None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
        errLog("No Truck Data for " + str(truckNumber(cS, int(tL))) + " --- Error")
    else:
        errLog("Got Data for "+ str(truckNumber(cS, int(tL))))
    while row:
        tName = truckNumber(cS, row[1])
        sDate = row[8]
        fDate = row[9]
        sOdo = str(row[10])
        fOdo = str(row[11])
        if (row[10] == None):
            sOdo = str("0.00")
        if (row[11] == None):
            fOdo = str("0.00")
        sOdo = round((float(sOdo)),2)
        fOdo = round((float(fOdo)),2)
        rpayLoad = row[16]
        if (rpayLoad == None):
            rpayLoad = str("0.00")
        payLoad = round((float(rpayLoad)),2)
        tDist = (round(((fOdo) - (sOdo)),2))
        returnData.append((tName, str(sDate), str(fDate), sOdo, fOdo, payLoad, tDist))
        row = cur.fetchone()
    conn.close()
    return returnData
