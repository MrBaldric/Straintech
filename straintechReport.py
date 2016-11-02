import time, create_Payload_Report, create_TKMS_Report, get_Config_Settings
from histLogging import errLog
from straintechSQLModule import sqlConn
import straintechEmailModule
from histLogging import errLog
errLog("Started Straintech Automatic Reporting")
#Get COnfiguration settings from config.xml
cS = []
cS = get_Config_Settings.getSettings()
#Used to go back more than one day in history
daysback = 1
errLog("Completed Loading Configuration settings")
#create truck straintech ID list from config.xml file
tList = cS[1]
#Current date
tDate = time.strftime("%a_%d_%m_%Y",time.localtime((time.time())))
#create report filename list
fname = []
fname.append("Daily Payload Report {}.pdf".format((tDate)))
fname.append("Daily Tkms Report {}.pdf".format((tDate)))
#Date and Time selection start and finish times
sDateAM = time.strftime("%Y-%m-%d 07:00:00",time.localtime((time.time() - (daysback * 86400))))
fDateAM = time.strftime("%Y-%m-%d 19:00:00",time.localtime((time.time() - (daysback * 86400))))
sDatePM = time.strftime("%Y-%m-%d 19:01:00",time.localtime((time.time() - (daysback * 86400))))
fDatePM = time.strftime("%Y-%m-%d 07:00:00",time.localtime((time.time() - ((daysback - 1) * 86400))))
#create PDF reports from connected sql queries
dFleetData = []
dFleetDataShiftIndex = (len(tList))
dFleetDataShiftIndexCounter = 0

while (dFleetDataShiftIndexCounter < (dFleetDataShiftIndex)):
    time.sleep(0.01)
    dFleetData.append((sqlConn(sDateAM, fDateAM, cS, tList[dFleetDataShiftIndexCounter])))
    dFleetData.append((sqlConn(sDatePM, fDatePM, cS, tList[dFleetDataShiftIndexCounter])))
    dFleetDataShiftIndexCounter += 1

#Create Payload report
create_Payload_Report.compile_Report(cS,dFleetData, sDateAM, fDatePM )
#Create TKMS Report
create_TKMS_Report.compile_Report(cS,dFleetData, sDateAM, fDatePM )
#Email PDF to receipentants
straintechEmailModule.DailyReportEmail(cS,fname)
#Completed Report run logging
errLog("Finished Straintech Automatic Reports\n######################################################################")
