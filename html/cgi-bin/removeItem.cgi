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
<body>
"""
if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    c=Cookie.SimpleCookie()
    c.load(cookie_string)

    try:
        cData=c["custId"].value
    except KeyError:
        print "You're not logged in! Register now or login:"
        print "<form method='post' action='../login.htm'>"
        print "<p><input type='submit' value='Login'></p>"
        print "</form>"
        print "<form method='post' action='../register.htm'>"
        print"<input type='submit' value='Register'>"
        print "</form>"
print """
</body>
</html>

"""

sql = "UPDATE cart SET quantity = quantity - %s WHERE item_id='%s' AND customer_id='%s'"%(quant,item,cData)

try:    
    myCursor.execute(sql)
    db.commit()
except:
    print "Error: unable to update data."
    db.rollback()

print "<html>"
print "<head>"
print "<title>Item Removed</title>"
print "<link href='https://fonts.googleapis.com/css?family=Merienda' rel='stylesheet'>"
print "<link rel='stylesheet' href='../kittyformat.css' />"
print "</head>"
print "<body>"
print "<h2 id ='one'><center> Item Removed, Cart Updated</center></h2>"
print "</body>"
