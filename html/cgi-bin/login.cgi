#!/usr/bin/python
import Cookie
import cgi, cgitb
import MySQLdb
from dbInfo import *

myForm = cgi.FieldStorage()

email = myForm.getvalue("custEmail")
password = myForm.getvalue("password")

db,myCursor = dbConnectCursor()

sql = "SELECT password from customer_t WHERE email = '%s'"%(email)
sql2 = "SELECT customer_name from customer_t WHERE email = '%s'"%(email)
sql3 = "SELECT customer_id from customer_t WHERE email = '%s'"%(email)
sql4 = "SELECT customer_type from customer_t WHERE email = '%s'"%(email)

try:
        myCursor.execute(sql3)
        output = myCursor.fetchone()
        for row in output:
          cusId = row
except:
        print "Error: unable to fetch data."

try:
        myCursor.execute(sql)
        output = myCursor.fetchone()
        for row in output:
          pWord = row  
except:
        print "Error: unable to fetch data."

try:
        myCursor.execute(sql2)
        output = myCursor.fetchone()
        for row in output:
          custName = row  
except:
        print "Error: unable to fetch data."

try:
    myCursor.execute(sql4)
    output = myCursor.fetchone()
    for row in output:
        custType = row
except:
    print "Error: unable to fetch data."
    
db.close()

try:
  if password == pWord:
    c = Cookie.SimpleCookie()
    c["custId"] = cusId
    c["custId"]["expires"] = 60 * 60 * 24
    print(c)
    print "Content-type:text/html\r\n\r\n"
    print "<html>"
    print "<head>"
    print "<title>Confirm</title>"
    print "<link href='https://fonts.googleapis.com/css?family=Merienda' rel='stylesheet'>"
    print "<link rel='stylesheet' href='../b2bKittyFormat.css' />"
    print "</head>"
    print "<body>"
    print "<h2 id = 'one'><center> Welcome Back %s!</center></h2>" %(custName)
    if (custType == "Business"):
       print "<fieldset>"
       print "<legend>Directions for B2B Ordering:</legend>"
       print "<p>Customer ID Number: <strong>%s</strong></p>"%(c["custId"].value)
       print "<p>Data Port: <strong>11120</strong></p>"
       print "<p>Reply Port: <strong>11121</strong></p>"
       print "<p>Answer File to read: <strong>/var/www/ebusiness/b-f19-06/html/files/ClientSocket/As.dat</strong></p>"
       print "<p>Question File for Server: <strong>/var/www/ebusiness/b-f19-06/html/files/ClientSocket/Qs.dat</strong></p>"
       print "<p>In a .dat file, send us in this exact order:</p>"
       print "<p><strong>1. Your Customer ID Number provided above</strong></p>"
       print "<p><strong>2. Your password you created when registering</strong></p>"
       print "<p><strong>3. The Item ID number of the item you are purchasing</strong></p>" 
       print "<p>   (Item ID numbers  can be found in our catalog when you click to view an item.)</p>"
       print "<p><strong>4. The quantity you are purchasing</strong></p>"
       print "<p><strong>5. Your desired shipping method.</strong><strong> (1</strong> is for standard, <strong>2</strong> is for express.)</strong></p>"
       print "<p>Everything should be typed out consecutively and seperated by spaces in your .dat file.</p>"
       print "<p>Example:</p>"
       print "<p><strong>120000 kittyCabPass71! 121001 3 1</strong></p>"
       print "<p>Our Answers: </p>"
       print "<p>If your order went through, you will be sent <strong> 0</strong> and a 10 digit confirmation number on separate lines.</p>"
       print "<p>Example:</p>"
       print "<p><strong>0</strong><br>"
       print "<strong>1210122484</strong></p>"
       print "<p>If your account doesn't exist in our database, you will be sent <strong>1 </strong></p>"
       print "<p>If your account is NOT a business account, you will be sent <strong>2 </strong></p>"
       print "<p>If there is an issue with the SHIPPING, you will be sent <strong>3 </strong></p>"
       print "<p>If there is an issue with the BANK, you will be sent <strong>4 </strong></p>"
       print "<p>If there is an issue with the MAYOR, you will be sent <strong>5 </strong></p>"
       print "<p>If there is an issue with IT SERVICES, you will be sent <strong>6 </strong></p>"
       print "<p>Any issues please contact us at hoffmank4@hawkmail.newpaltz.edu</p>"
       print "<p>Happy Shopping!</p>"
    if (custType == "Staff"):
       print "<form method='post' action='../staffB2B.htm'>"
       print "<p><center>Ordering from another business? Click Below!</center></p>"
       print "<p><center><input type='submit' value='B2B Form'></center></p>"      
  else:
    print "Content-type:text/html\r\n\r\n"
    print "<center>Wrong Password or Username!</center>"
except:
  print "Content-type:text/html\r\n\r\n"
  print "<center>Email not registered. Try again or sign up now!</center>"
print "</body>"
print "</html>"
