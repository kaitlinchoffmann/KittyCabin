#!/usr/bin/python
import Cookie
import cgi, cgitb
import MySQLdb
from dbInfo import *

db,myCursor = dbConnectCursor()

sql = "DELETE FROM cart WHERE customer_id = 12345;"

try:
    myCursor.execute(sql)
    db.commit()
except:
    db.rollback()    

c=Cookie.SimpleCookie()
c['custId']=''
c['custId']['expires']='Thu, 01 Jan 1970 00:00:00 GMT'
print c

print "Content-type:text/html\n\n"
print """
<html>
<head>
    <link rel="stylesheet" href="../kittyformat.css" />
</head>        
<body>
<h2 id = 'one'><center>Thanks for Stopping by! Log Back in or Register with a New Account:</center><h2>
        <form method='post' action='../login.htm'>
        <center><input type='submit' value='Login'>
        </form>
        <form method='post' action='../register.htm'>
        <input type='submit' value='Register'>
        </form></center>
</body>
</html>

"""
