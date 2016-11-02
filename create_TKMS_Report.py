import time, os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, green, blue, orange, purple
import straintechEmailModule
from histLogging import errLog

def totalTonnes(data):
	dFleetSize = len(data)
	dFleetTotalTonnes = []
	countTrk = 0
	while (countTrk < dFleetSize):
		countTT = 0
    		dLenght = len(data[countTrk])
    		dList = []
    		while (countTT < dLenght):
        		dList.append(float(str(data[countTrk][countTT][5])))
        		countTT += 1
    		dFleetTotalTonnes.append(round(sum(dList),2))
		countTrk += 1
    	return dFleetTotalTonnes

def totalDistance(data):
        dFleetSize = len(data)
        dFleetTotalDistance = []
        countTrk = 0
        while (countTrk < dFleetSize):
                countTT = 0
                dLenght = len(data[countTrk])
                dList = []
                while (countTT < dLenght):
                        dList.append(float(str(data[countTrk][countTT][6])))
                        countTT += 1
                dFleetTotalDistance.append(round(sum(dList),2))
                countTrk += 1
        return dFleetTotalDistance

def totalTkms(dTD, dTT):
	dTTkms = round((dTD * dTT),2)
	return dTTkms

def shift(index):
        if (index % 2 == 0):
                shft = 'D'
        else:
                shft = 'N'
        return shft

def shiftTotalTonnes(shft, data):
        dataLen = len(data)
        shftData = []
        if (shft == 'D'):
                tCount = 0
                while (tCount < dataLen):
                        shftData.append(data[tCount])
                        tCount += 2
        if (shft == 'N'):
                tCount = 1
                while (tCount < dataLen):
                        shftData.append(data[tCount])
                        tCount += 2
        shftTotalTonnes = round(sum(shftData),2)
        return shftTotalTonnes
        
def shiftTotalDistance(shft, data):
        dataLen = len(data)
        shftData = []
        if (shft == 'D'):
                tCount = 0
                while (tCount < dataLen):
                        shftData.append(data[tCount])
                        tCount += 2
        if (shft == 'N'):
                tCount = 1
                while (tCount < dataLen):
                        shftData.append(data[tCount])
                        tCount += 2
        shftTotalDistance = round(sum(shftData),2)
        return shftTotalDistance
        

def total24Tkms(tonnes,distance):
        counter = 0
        dTTkmsValue = 0
        tonDataLenght = len(tonnes)
        disDataLenght = len(distance)
        TTkmsList = []
        if (tonDataLenght == disDataLenght):
                while (counter < tonDataLenght):
                        dTTkmsValue = ((float(tonnes[counter])) * (float(distance[counter])))
                        TTkmsList.append(dTTkmsValue)
                        counter += 1
                dTotal24Tkms = round(sum(TTkmsList),2)
        else:
                errLog("Mismatch between create_TKMS_Report variables TableData.dTT and TableData.dTD")
        return dTotal24Tkms
        

def TableData(c,dFD, dTT, dTD, sLoc):
        dTTlenght = len(dTT)
        dTDlenght = len(dTD)
        lSpace = 30 #Line Spacing
        rowCount = 0
        while (rowCount < dTTlenght): 
                c.drawCentredString(180,(sLoc - (lSpace * rowCount)),text="{}".format(str((dFD[rowCount][0][0]))))
                c.drawCentredString(350,(sLoc - (lSpace * rowCount)),text="{}".format(str(shift(rowCount))))
                c.drawRightString(600,(sLoc - (lSpace * rowCount)),text="{}".format(str((dTT[rowCount]))))#Draw Total Tonnes per truck per shift
                c.drawRightString(800,(sLoc - (lSpace * rowCount)),text="{}".format(str((dTD[rowCount]))))#Draw Total Distance per truck per shift
                c.drawRightString(1000,(sLoc - (lSpace * rowCount)),text="{}".format(str((totalTkms((dTT[rowCount]),(dTD[rowCount]))))))#Draw Total Tkms per truck per shift
                rowCount += 1
        c.line(100,(sLoc - (lSpace * (rowCount + 0.5))),1100,(sLoc - (lSpace * (rowCount + 0.5))))#Header Boarder
        c.setFont("Times-Bold",16)
        c.drawCentredString(180,(sLoc - (lSpace * (rowCount + 2))),text="24Hrs Totals")#Draw Totals heading
        c.setFont("Times-Roman",16)
        dsumdTT = sum(dTT)
        c.drawRightString(600,(sLoc - (lSpace * (rowCount + 2))),text="{}".format(str(dsumdTT)))#Draw Total Tonnes in 24Hrs
        dsumdTD = sum(dTD)
        c.drawRightString(800,(sLoc - (lSpace * (rowCount + 2))),text="{}".format(str(dsumdTD)))#Draw Total Distance in 24Hrs
        c.drawRightString(1000,(sLoc - (lSpace * (rowCount + 2))),text="{}".format(str(total24Tkms(dTT,dTD))))#Draw Total Tkms in 24Hrs
        dSTT_D = shiftTotalTonnes('D',dTT)
        c.drawRightString(600,380,text="{}".format(str((dSTT_D))))#Draw Day Shift Tonnes
        dSTD_D = shiftTotalDistance('D',dTD)
        c.drawRightString(800,380,text="{}".format(str((dSTD_D))))#Draw Day Shift Distance
        dSTT_N = shiftTotalTonnes('N',dTT)
        c.drawRightString(600,330,text="{}".format(str((dSTT_N))))#Draw Night Shift Tonnes
        dSTD_N = shiftTotalDistance('N',dTD)
        c.drawRightString(800,330,text="{}".format(str((dSTD_N))))#Draw Night Shift Distance
        dSTTkms_D = totalTkms(dSTT_D,dSTD_D)
        c.drawRightString(1000,380,text="{}".format(str((dSTTkms_D))))#Draw Day Shift TKMS
        dSTTkms_N = totalTkms(dSTT_N,dSTD_N)
        c.drawRightString(1000,330,text="{}".format(str((dSTTkms_N))))#Draw Night Shift TKMS
        dTTT = dSTT_D + dSTT_N
        c.drawRightString(600,240,text="{}".format(str((dTTT))))#Draw Total 24hrs Tonnes
        dTTD = dSTD_D + dSTD_N
        c.drawRightString(800,240,text="{}".format(str((dTTD))))#Draw Total 24hrs Distance
        dTTTkms = dSTTkms_D + dSTTkms_N
        c.drawRightString(1000,240,text="{}".format(str((dTTTkms))))#Draw Total 24hrs Distance

        
def GraphFrame(c, sd, fd):
        file="\images\Logo.jpg"
        path=os.getcwd()+file
        #Report Header
        c.setFont("Times-Bold",50)
        c.drawRightString(1100,1520,text="TKMs Daily Report")
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
        c.line(100,120,1100,120)#Bottom Boarder
        c.line(100,1300,1100,1300)#Top Boarder
        c.line(100,120,100,1300)#Left Boarder
        c.line(1100,120,1100,1300)#Right Boarder
        #Create table headings
        c.setFont("Times-Bold",16)
        c.drawString(120,1270,text="Tonnes kms per Truck broken down into Day and Night Shift summary")
        c.drawCentredString(180,1230,text="Truck")
        c.drawCentredString(350,1230,text="Shift")
        c.drawRightString(600,1230,text="Total Tonnes")
        c.drawRightString(800,1230,text="Total Distance(kms)")
        c.drawRightString(1000,1230,text="Total Tkms")
        c.line(100,1200,1100,1200)#Header Boarder
        #TKMS Report per shift
        c.drawString(120,490,text="Tonnes kms per Shift summary")
        c.drawCentredString(180,450,text="Shift")
        c.drawRightString(600,450,text="Total Tonnes")
        c.drawRightString(800,450,text="Total Distance(kms)")
        c.drawRightString(1000,450,text="Total Tkms")
        c.line(100,420,1100,420)#Header Boarder
        c.drawString(150,380,text="Day Shift")
        c.drawString(150,330,text="Night Shift")
        c.line(100,285,1100,285)#Header Boarder
        c.drawString(150,240,text="24Hrs Total")
        c.setFont("Times-Roman",16)


def compile_Report(cS,dFleetData, sD, fD):
        fileLoc = cS[3][0]
	reportFilename = "{}\\Daily Tkms Report {}.pdf".format(fileLoc,(time.strftime("%a_%d_%m_%Y",time.localtime((time.time())))))
	c = canvas.Canvas(reportFilename)
	dFleetTotalTonnes = totalTonnes(dFleetData)
	dFleetTotalDistance = totalDistance(dFleetData)
	c.scale(0.5,0.5) #Scale page
	sLoc = 1150
        GraphFrame(c, sD, fD) #create page frame template
	TableData(c, dFleetData, dFleetTotalTonnes, dFleetTotalDistance, sLoc)#place date on page
	c.showPage()#compile PDF page
	c.save()#save PDF.
	errLog("TKMS Report Created")


