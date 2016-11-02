#Email Module sending the straintec data
import smtplib,email,email.encoders,email.mime.text,email.mime.base,time
from email.mime.multipart import MIMEMultipart
from histLogging import errLog

fromAddress = "StrainTechPC@emalladdress.com"
emailSubject = "Payload Report"
emailFrom = 'StrainTech System PC'


def emailAddress(data):
    toAdd = []
    dataLen = len(data)
    countAdd = 0
    while (countAdd < dataLen):
        toAdd.append(data[countAdd])
        countAdd += 1
    return toAdd
        

def emailText():
    emailTextBody = 'Test Email from StraintechPC'
    emailMsg = email.MIMEMultipart.MIMEMultipart('mixed')
    emailMsg['Subject'] = emailSubject
    emailMsg['From'] = emailFrom
    emailMsg['To'] =  ",".join(toAddress)
    emailMsg.attach(email.mime.text.MIMEText(emailTextBody,'html'))
    emailServer = smtplib.SMTP("<ip address of email server>")
    emailServer.sendmail(fromAddress, toAddress,emailMsg.as_string())
    emailServer.close()
        

def DailyReportEmail(cS,fname):
    body = """\
    <b><p style="color:green;font-size:120%">Mine Site
    <br>===================================
    <br>Payload & Tkms Reports</p></b>
    <br><i><p>Please see the attached the Daily Straintech Reports
    <br><br>Thank you<br><br>Have a great day</p></i>
    """
    toAddress = emailAddress(cS[4])
    fileLoc = cS[3][0]
    emailMsg = MIMEMultipart()
    emailMsg['Subject'] = emailSubject
    emailMsg['From'] = emailFrom
    emailMsg['To'] =  ",".join(toAddress)
    cA = 0
    fnameLenght = len(fname)
    while (cA < fnameLenght):
        loadFile = open('{}\\{}'.format(fileLoc,fname[cA]), 'rb')
        fileMsg = email.mime.base.MIMEBase('application','pdf')
        fileMsg.set_payload((loadFile).read())
        fileMsg.add_header('Content-Disposition', 'attachment', filename = fname[cA])
        email.encoders.encode_base64(fileMsg)
        emailMsg.attach(fileMsg)
        loadFile.close()
        cA += 1
    emailMsg.attach(email.mime.text.MIMEText(body,'html'))
    emailServer = smtplib.SMTP("<ip address or email server>")
    emailServer.sendmail(fromAddress, toAddress,emailMsg.as_string())
    emailServer.close()
    errLog("Emailed reports completed")
