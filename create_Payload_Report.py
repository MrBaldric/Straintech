
import time, os
from reportlab.pdfgen import canvas
import datetime
from reportlab.lib.colors import red, green, blue, orange, purple
from histLogging import errLog


def totalWeight(data):
    count = 0
    dLenght = len(data)
    dList = []
    while (count < dLenght):
        dList.append(float(str(data[count][5])))
        count += 1
    tWeight = sum(dList)
    return tWeight

def TableData(c,rawData, sLoc, sTitle):
    rawDataLenght = len(rawData)
    lSpace = 22 #Line Spacing
    tWeight = totalWeight(rawData)#get total weight of shift
    rowCount = 0
    c.drawString(110,(sLoc + 35),text="{}".format(sTitle))
    c.drawString(860,sLoc + 35,text="Total : {} t".format(tWeight))
    while (rowCount < rawDataLenght): 
        c.drawString(110,(sLoc - (lSpace * rowCount)),text="{}".format(rawData[rowCount][0]))
        c.drawString(300,(sLoc - (lSpace * rowCount)),text="{}".format(rawData[rowCount][1]))
        c.drawString(500,(sLoc - (lSpace * rowCount)),text="{}".format(rawData[rowCount][2]))
        c.drawString(700,(sLoc - (lSpace * rowCount)),text="{}".format(rawData[rowCount][3]))
        c.drawString(800,(sLoc - (lSpace * rowCount)),text="{}".format(rawData[rowCount][4]))
        c.drawString(900,(sLoc - (lSpace * rowCount)),text="{}".format(rawData[rowCount][5]))
        c.drawString(1000,(sLoc - (lSpace * rowCount)),text="{}".format(rawData[rowCount][6]))
        rowCount += 1


def GraphFrame(c, pTitle, sd, fd):
    file="\images\Logo.jpg"
    path=os.getcwd()+file
    #Report Header
    c.setFont("Times-Bold",50)
    c.drawRightString(1100,1520,text="{} Payload Daily Report".format(pTitle))
    c.drawRightString(1100,1450,text="Mine Site")
    c.drawImage(path,50,1400,200,200)
    #Report Footer
    c.setFont("Times-Roman",16)
    footerDate = time.strftime("%b %d %Y",time.localtime((time.time())))
    c.drawString(950,80,text=footerDate)
    footerName = "Data collected from Gold Mine Straintech vehicle mounted equipment"
    c.drawString(100,80,text=footerName)
    #Draw time report period
    c.setFont("Times-Bold",18)
    c.drawRightString(1100,1320,text="Report Period: {} to {}".format(sd,fd))
    #Create page Report Frame
    c.setFont("Times-Roman",24)
    c.line(100,120,1100,120)#Bottom Boarder
    c.line(100,1300,1100,1300)#Top Boarder
    c.line(100,120,100,1300)#Left Boarder
    c.line(1100,120,1100,1300)#Right Boarder
    #Create table headings
    c.setFont("Times-Roman",16)
    c.saveState()
    c.setFont("Times-Bold",16)
    c.drawString(110,1250,text="Truck")
    c.drawString(300,1250,text="Start Time")
    c.drawString(500,1250,text="Finish Time")
    c.drawString(700,1250,text="Start Odo")
    c.drawString(800,1250,text="Finish Odo")
    c.drawString(900,1250,text="Weight (t)")
    c.drawString(1000,1250,text="Distance (km)")
    c.restoreState()


def compile_Report(cS,dFleetData, sD, fD):
    fileLoc = cS[3][0]
    #create report file with file name
    reportFileName = "{}\\Daily Payload Report {}.pdf".format(fileLoc,(time.strftime("%a_%d_%m_%Y",time.localtime((time.time())))))
    #create canvas c for report
    c = canvas.Canvas(reportFileName)
    D_tLoc = 1150
    N_tLoc = 600
    #Under standing dFleetData Array
    #================================
    #dFleetData[truck1 Dayshift data][truck1 Nightshift data][truck2 Dayshift data][truck2 Nightshift data] . . . etc
    #truck1 Dayshift data = [trip 1 data][trip 2 data][trip 3 data][trip 4 data] . . . etc
    #trip1 data = [truck number,start time,finish time, start odo, finish odo, weight, distance]
    #eg dFleetData[2][2][1] = truck 2 dayshift - trip 3 truck start time
    #
    #Truck Report create
    dfleet = len(dFleetData)#get total number of truck entries
    tC = 0
    while (tC < dfleet):
        c.scale(0.5,0.5) #Scale page
        GraphFrame(c, dFleetData[tC][0][0], sD, fD) #create page frame
        TableData(c, dFleetData[tC], D_tLoc, "Dayshift") #Place data on page
        tC += 1
        TableData(c, dFleetData[tC], N_tLoc, "Nightshift") #Place data on page
        tC += 1
        c.showPage() #create page
    #Save PDF File
    c.save()
    errLog("Payload Report Created")
    



