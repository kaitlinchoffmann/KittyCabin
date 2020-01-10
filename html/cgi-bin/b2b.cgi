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
<head>

        <title>B2B Confimation</title>
        <link href='https://fonts.googleapis.com/css?family=Merienda' rel='stylesheet'>
        <link rel="stylesheet" href="../topKittyFormat2.css" />
</head>
<body>
"""

if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    c=Cookie.SimpleCookie()
    c.load(cookie_string)

    try:
        cData=c["custId"].value
        print """
        <nav>
        <ul>
          <li><a href="index-top-menu2.cgi">Home</a></li>
          <li><a href="about.cgi">About</a></li>
          <li><a href="logout.cgi">Logout</a></li>
          <li><a href="catalog.cgi">Shop</a></li>
          <li><a href="cart.cgi">Cart</a></li-last>
        </ul>
        </nav>
       
        """
    except KeyError:
        print """
        <nav>
        <ul>
          <li><a href="index-top-menu2.cgi">Home</a></li>
          <li><a href="about.cgi">About</a></li>
          <li><a href="../login.htm">Login</a></li>
          <li><a href="register2.cgi">Register</a></li>
          <li><a href="catalog.cgi">Shop</a></li>
          <li><a href="cart.cgi">Cart</a></li-last>
        </ul>    
        </nav>
        """    
       
else: 
    print """
    <nav>
    <ul>
      <li><a href="index-top-menu2.cgi">Home</a></li>
      <li><a href="about.cgi">About</a></li>
      <li><a href="../login.htm">Login</a></li>
      <li><a href="register2.cgi">Register</a></li>
      <li><a href="catalog.cgi">Shop</a></li>
      <li><a href="cart.cgi">Cart</a></li-last>
    </ul>
    </nav>
    """
print "<div id=viewLay>"
print "<h2 id='one'><center>B2B Confirmation Page</center></h2>"
         
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
	print "<h2 id='one'><center>Issue with B2B Transaction. Please Try Again.</center></h2>"
else:
	print "<h2 id='one'><center>Transaction Successful!</center></h2>"
db.close()
