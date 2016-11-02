import time, os

def errLog(sText):
    file="\Logs\history.log"
    path=os.getcwd()+file
    tCurrent = time.strftime("%Y-%m-%d\t%H:%M:%S",time.localtime((time.time())))
    oLogFile = open(path,"a")
    oLogFile.write("{}\t{}\n".format(tCurrent,sText))
    oLogFile.close()
    
