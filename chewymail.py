#!/usr/bin/python

# Import smtplib for the actual sending function
import smtplib
 
# For guessing MIME type
import mimetypes
 
# Import the email modules we'll need
import email
import email.mime.application
 
#Import sys to deal with command line arguments
import sys

# MySQL DB connection
import MySQLdb as sql
DbUser = ""
DbPass = ""
DbName = ""

try:
   db = sql.connect("localhost", DbUser, DbPass, DbName)
   curs = db.cursor()
except:
   sys.exit(0)

curs.execute("SELECT count(*) FROM rundata WHERE tsStamp > DATE_SUB(NOW(), INTERVAL 12 HOUR) and speed > 0")
rotations = curs.fetchone()[0]
curs.execute("SELECT MAX(speed) FROM rundata WHERE tsStamp > DATE_SUB(NOW(), INTERVAL 12 HOUR) and speed > 0")
maxspeed = curs.fetchone()[0]
 
# Create a text/plain message
msg = email.mime.Multipart.MIMEMultipart()
msg['Subject'] = 'ChewyMon Distance for Last Night'
msg['From'] = 'xxx@gmail.com'
msg['To'] = 'xxx@gmail.com'
 
inches = rotations*33
feet = (rotations*33.0)/12.0

# The main body is just another attachment
body = email.mime.Text.MIMEText("Chewy Stats:\n\nInches: %s\nFeet:   %s\n\nMax Speed: %s MPH" % (inches, feet, maxspeed))
msg.attach(body)
 
# send via Gmail server
# NOTE: my ISP, Centurylink, seems to be automatically rewriting
# port 25 packets to be port 587 and it is trashing port 587 packets.
# So, I use the default port 25, but I authenticate.
s = smtplib.SMTP('smtp.gmail.com:587')
s.starttls()
s.login('xxx@gmail.com','xxxpasswordxxx')
s.sendmail('xxx@gmail.com',['xxx@gmail.com'], msg.as_string())
s.quit()
