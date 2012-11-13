import smtplib
import sys

args = (sys.argv)

SMTPServer = args[1]
SMTPUser = args[2] 
SMTPPassword = args[3]
Rec = args[4]
Sender = args[5]
Message = open(args[6]).read()
print SMTPServer
serv = smtplib.SMTP(SMTPServer, 587)
serv.ehlo()
if (serv.has_extn("STARTTLS")):
		serv.starttls()
serv.login(SMTPUser, SMTPPassword)
header = 'To:' + Rec + '\n' + 'From: author@example.com \n'
message = header + Message;
serv.sendmail('author@example.com', Rec, message)
serv.close()
