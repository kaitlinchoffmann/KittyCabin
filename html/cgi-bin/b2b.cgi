#!/usr/bin/python
import cgi, cgitb
import MySQLdb
import Cookie
import os
import subprocess
from dbInfo import *

myForm = cgi.FieldStorage()

custId = myForm.getvalue('cusId')
custPass = myForm.getvalue('cusPass')
itemID = myForm.getvalue('itemId')
quan = myForm.getvalue('quant')
ports = myForm.getvalue('port')
asFile = myForm.getvalue('asfile')

db,myCursor = dbConnectCursor()

print "Content-type:text/html\n\n"
print """
<html>
<body>
"""
if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    c=Cookie.SimpleCookie()
    c.load(cookie_string)

    try:
        cData=c["custId"].value
    except KeyError:
        print "No cookie :("
print """
</body>
</html>

"""
         
b2bInfo = custId + " " + custPass + " " + itemID + " " + quan
b2bFile = bankFile = open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/Qc.dat", "w")
b2bFile.write(b2bInfo)
b2bFile.close()

#changing port:
changePort = open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/necPorts.txt", "w")
changePort.write(ports + " /var/www/ebusiness/b-f19-06/html/files/ClientSocket/f-Qc.dat /var/www/ebusiness/b-f19-06/html/files/ClientSocket/Qc.dat /var/www/ebusiness/b-f19-06/html/files/ClientSocket/Qs.dat /var/www/ebusiness/b-f19-06/html/files/ClientSocket/f-Ac.dat /var/www/ebusiness/b-f19-06/html/files/ClientSocket/Ac.dat " + asFile) #/var/www/ebusiness/b-f19-06/html/files/ClientSocket/Qs.dat /var/www/ebusiness/b-f19-06/html/files/ClientSocket/As.dat
changePort.close()
        
p1 = subprocess.Popen(["/usr/bin/java", "Client"], stdout=subprocess.PIPE)
print p1.stdout.read()       

with open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/Ac.dat", "r") as file:
	b2bRes=file.read()
b2bRes=map(str,b2bRes)
b2bRes2=b2bRes[0]

transB2B = False
if(b2bRes2 == "0"):
	transB2B = True
else:
	print "Something wrong with B2B request"

print(transB2B)
if transB2B != True:
	print "Issue with B2B Transaction. Please Try Again."
else:
	print "Transaction Successful!"
db.close()
