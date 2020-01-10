#!/usr/bin/python
import cgi, cgitb
import MySQLdb
import Cookie
import os
from dbInfo import *

webForm = cgi.FieldStorage()

itemId = webForm.getvalue('itemId')

db,myCursor = dbConnectCursor()

print "Content-type:text/html\n\n"
print """
<html>
<head>
        <title>View Item | The Kitty Cabin</title>
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
          <li><a href="register2.cgi">Register</a></li>
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
      <li><a href="register2.cgi">Register</a></li>
      <li><a class="active" href="catalog.cgi">Shop</a></li>
      <li><a href="cart.cgi">Cart</a></li-last>
    </ul>
    </nav>
    """

sql = "SELECT * FROM inventory_t WHERE item_id = '%s'"%(itemId)
try:
        myCursor.execute(sql)
        output = myCursor.fetchall()
        print "<form method = 'post' action='addItem.cgi'>"
        print "<div id = 'viewLay'>"
        for row in output:
                print "<input type='hidden' name = 'itemId' value='%s'>"%(row[0])
                print "<h2 id = 'one'><center>%s</center></h2>"%(row[6])
                print "<p><center><img src ='%s'></center></p>" %(row[7])
                print "<p>Price: %s</p>" %(row[2])
                print "<p>Size: %s</p>" %(row[3])
                print "<p>Item ID: %s"%(row[0])
                if (row[1] == 0):
                    print "<p><strong>SOLD OUT</strong></p>"
                else:
                    print "<input type='number' name='quantity' min='1' max='20' value='1'>"    
                    print "<input type='submit' onclick='alert('Added To Cart!')' name='addCart' value='Add to Cart'>"
                    print "</p>"   
        print "</div>"
        print "</form>" 
        print "</body>"
        print "</html>"       
except:
        print "Error: unable to fetch data"
db.close()
