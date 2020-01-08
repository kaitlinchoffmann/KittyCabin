#!/usr/bin/python
import cgi, cgitb
import MySQLdb
import Cookie
import os
from dbInfo import *

myForm = cgi.FieldStorage()

item = myForm.getvalue('itemId') 
quant = myForm.getvalue('quantity')

db,myCursor = dbConnectCursor()

print "Content-type:text/html\n\n"
print """
<html>
<head>
    <link rel="stylesheet" href="../kittyformat.css" />
</head>    
<body>
"""

if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    c=Cookie.SimpleCookie()
    c.load(cookie_string)

    try:
        cData=c["custId"].value
    except KeyError:              
        print "<h2 id ='one'><center>You're not logged in! Register now or login:</center></h2>"
        print "<p><form method='post' action='../login.htm'>"
        print "<center><input type='submit' value='Login'>"
        print "</form>"
        print "<form method='post' action='../register.htm'>"
        print"<input type='submit' value='Register'>"
        print "</form></center></p>"
else:
    print "<h2 id = 'one'><center>You're not logged in! Log in or Register now!</center><h2>"
    print "<form method='post' action='../login.htm'>"
    print "<center><input type='submit' value='Login'>"
    print "</form>"
    print "<form method='post' action='../register.htm'>"
    print"<input type='submit' value='Register'>"
    print "</form></center>"        
print """
</body>
</html>

"""

sql = "UPDATE cart SET quantity = quantity + '%s' WHERE item_id='%s' AND customer_id='%s'"%(quant,item,cData)
sql2 = "SELECT cart_id FROM cart WHERE item_id='%s' AND customer_id='%s'"%(item,cData)
sql3 = "INSERT into cart (cart_id, customer_id, item_id, quantity) VALUES (null, '%s', '%s', '%s')"%(cData,item,quant)

try:    
        myCursor.execute(sql2)
        output = myCursor.fetchone()
        for row in output:
          cartId = row
        myCursor.execute(sql)
        db.commit()
except:
  try:
      myCursor.execute(sql3)
      db.commit()
  except:
      print "Error: unable to update dataaa."
      db.rollback()

print "<html>"
print "<head>"
print "<title>Added Item to Cart</title>"
print "<link href='https://fonts.googleapis.com/css?family=Merienda' rel='stylesheet'>"
print "<link rel='stylesheet' href='../kittyformat.css' />"
print "</head>"
print "<body>"
print "<h2 id ='one'><center> Cart Was Updated!</center></h2>"
print "</body>"
print "</html>"
