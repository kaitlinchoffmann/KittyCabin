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
    <title>Logout | The Kitty Cabin</title>
    <link href='https://fonts.googleapis.com/css?family=Merienda' rel='stylesheet'>
    <link rel="stylesheet" href="../kittyformat.css" />
    <link rel="stylesheet" href="../topKittyFormat2.css" />
</head>        
<body>
<h2 id = 'one'><center>Thanks for Stopping by! Log Back in or Register with a New Account:</center><h2>

<CENTER>
  <h1>The Kitty Cabin</h1>
</CENTER>

<div id='body2'>
<CENTER>
<h2>Login</h2>  
<form method = "post" action="login.cgi"> <!-- cgi-bin/index-top-menu2.cgi  cgi-bin/login.cgi -->
<div id ="one">          
        <p>Email: 
        <input type="text" name="custEmail"><br>
        Password:
        <input type="text" name="password"><br>
        <input type="submit" value="Sign In" name="Sign In">
        </p> 
</div>                      
</form>
<p>Register a New Account! </p> 
<form method = "post" action="register2.cgi">
    <p><input type="submit" value="Register" name="register"></p>
</form>
</CENTER>
</div>

</body>
</html>

"""
