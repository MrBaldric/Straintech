import xml.etree.ElementTree as et
import os
from histLogging import errLog

def getSettings():
        errLog("Loading Configuration xml file settings")
	configSettings = []
	mssqlSettings = []
	truckStraintechID = []
	truckFleetNumber = []
	fileDetails = []
	emailAddresses = []
	file="\config\config.xml"
        path=os.getcwd()+file
	tree = et.parse(path)
	root = tree.getroot()
	for a in root.iter("configuration"):
		ct1 = 0
		while ct1 < len(a):
			ct1 +=1 
	for b in root.iter(a[0].tag):
		ct2 = 0
		while ct2 < len(b):
			mssqlSettings.append(b[ct2].text)
			ct2 += 1
	for c in root.iter(a[1].tag):
		ct3 = 0
		while ct3 < len(c):
			truckStraintechID.append(c[ct3].text)
			ct3 += 2
	for d in root.iter(a[1].tag):
		ct4 = 1
		while ct4 < len(d):
			truckFleetNumber.append(c[ct4].text)
			ct4 += 2
	for e in root.iter(a[2].tag):
                ct5 = 0
                while ct5 < len(e):
                        fileDetails.append(e[ct5].text)
                        ct5 += 1
        for f in root.iter(a[3].tag):
                ct6 = 0
                while ct6 < len(f):
                        emailAddresses.append(f[ct6].text)
                        ct6 += 1
	configSettings.append(mssqlSettings)
	configSettings.append(truckStraintechID)
	configSettings.append(truckFleetNumber)
	configSettings.append(fileDetails)
	configSettings.append(emailAddresses)
	return configSettings
