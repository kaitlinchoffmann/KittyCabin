#!/usr/bin/python
import cgi, cgitb
import MySQLdb
import Cookie
import os
from dbInfo import *

myForm = cgi.FieldStorage()

db,myCursor = dbConnectCursor()

print "Content-type:text/html\n\n"
print """
<html>
<head>

        <title>The Kitty Cabin</title>
        <link href='https://fonts.googleapis.com/css?family=Merienda' rel='stylesheet'>
        <link rel="stylesheet" href="../topKittyFormat.css" />
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
        <div id = "header",class="header">
        <h1>The Kitty Cabin</h1>
        <br>Clothes for the Ultimate Cat Lover
        </div>

        <ul>
          <li><a href="../index-body.htm" target="BOT" onClick="window.location.reload()">Home</a></li>
          <li><a href="../about.htm" target="BOT" onClick="window.location.href='index-top-menu2.cgi'">About</a></li>
          <li><a href="logout.cgi" target="BOT">Logout</a></li>
          <li><a href="catalog.cgi" target="BOT" onClick="window.location.href='index-top-menu2.cgi'">Shop</a></li>
          <li><a href="cart.cgi" target="BOT" onClick="window.location.href='index-top-menu2.cgi'">Cart</a></li-last>
        </ul>
        """
    except KeyError:
        print """
        <div id = "header",class="header">
        <h1>The Kitty Cabin</h1>
        <br>Clothes for the Ultimate Cat Lover
        </div>

        <ul>
          <li><a href="../index-body.htm" target="BOT" onClick="window.location.href='index-top-menu2.cgi'">Home</a></li>
          <li><a href="../about.htm" target="BOT">About</a></li>
          <li><a href="../login.htm" target="BOT">Login</a></li>
          <li><a href="../register.htm" target="BOT">Register</a></li>
          <li><a href="catalog.cgi" target="BOT" onClick="window.location.href='index-top-menu2.cgi'">Shop</a></li>
          <li><a href="cart.cgi" target="BOT" onClick="window.location.href='index-top-menu2.cgi'">Cart</a></li-last>
        </ul>    
        """    
       
else:
    print """
    <div id = "header",class="header">
    <h1>The Kitty Cabin</h1>
    <br>Clothes for the Ultimate Cat Lover
    </div>

    <ul>
      <li><a href="../index-body.htm" target="BOT" onClick="window.location.href='index-top-menu2.cgi'">Home</a></li>
      <li><a href="../about.htm" target="BOT">About</a></li>
      <li><a href="../login.htm" target="BOT">Login</a></li>
      <li><a href="../register.htm" target="BOT">Register</a></li>
      <li><a href="catalog.cgi" target="BOT" onClick="window.location.href='index-top-menu2.cgi'">Shop</a></li>
      <li><a href="cart.cgi" target="BOT" onClick="window.location.href='index-top-menu2.cgi'">Cart</a></li-last>
    </ul>
    """
print """
</body>
</html>

"""
