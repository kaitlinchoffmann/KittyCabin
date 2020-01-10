#!/usr/bin/python
import cgi, cgitb
import MySQLdb
import Cookie
import os
from dbInfo import *

db,myCursor = dbConnectCursor()

print "Content-type:text/html\n\n"
print """
<html>
<head>

        <title>Catalog</title>
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
          <li><a class="active" href="catalog.cgi">Shop</a></li>
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
          <li><a href="../register.htm">Register</a></li>
          <li><a class="active" href="catalog.cgi">Shop</a></li>
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
      <li><a href="../register.htm">Register</a></li>
      <li><a class="active" href="catalog.cgi">Shop</a></li>
      <li><a href="cart.cgi">Cart</a></li-last>
    </ul>
    </nav>
    """

sql = "SELECT * FROM inventory_t;"

try:
        myCursor.execute(sql)
        output = myCursor.fetchall()
        print "<h2 id = 'one'><center> Check out these cool items!</center></h2>"
        for row in output:
                print "<form method = 'post' action='view_item.cgi'>"
                print "<div id='catLay'>"
                print "<input type='hidden' name = 'itemId' value='%s'>"%(row[0])
                print "<p><img src ='%s' width='200' height='300'>" %(row[7])
                print "Price: %s" %(row[2])
                print "Item: %s" %(row[6])
                print "<input type='submit' name='item' value='View Item'>"
                print "</div>"
                print "</form>"
                print "</p>"       
        print "</body>"
        print "</html>"        
except:
        print "Error: unable to fetch data"
db.close()
