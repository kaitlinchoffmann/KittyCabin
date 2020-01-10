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

        <title>Cart | The Kitty Cabin</title>
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
          <li><a  href="about.cgi">About</a></li>
          <li><a href="logout.cgi">Logout</a></li>
          <li><a href="catalog.cgi">Shop</a></li>
          <li><a class="active" href="cart.cgi">Cart</a></li-last>
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
          <li><a class="active" href="cart.cgi">Cart</a></li-last>
        </ul>    
        </nav>
        
        <h2 id = 'one'><center>You're not logged in! Log in or Register now!</center><h2>
        <form method='post' action='../login.htm'>
        <center><input type='submit' value='Login'>
        </form>
        <form method='post' action='../register.htm'>
        <input type='submit' value='Register'>
        </form></center>
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
      <li><a class="active" href="cart.cgi">Cart</a></li-last>
    </ul>
    </nav>
    
    <h2 id = 'one'><center>You're not logged in! Log in or Register now!</center><h2>
    <form method='post' action='../login.htm'>
    <center><input type='submit' value='Login'>
    </form>
    <form method='post' action='../register.htm'>
    <input type='submit' value='Register'>
    </form></center>
    """

sql = "SELECT * FROM cart WHERE customer_id = '%s' AND quantity > 0"%(cData)

try:
        myCursor.execute(sql)
        output = myCursor.fetchall()
        itemId=[]
        quan=[]
        for row in output:
            itemId.append(row[2])
            quan.append(row[3])
except:
        print "Error: unable to fetch data"

if (len(itemId) == 0):
    print "<div id='viewLay'>"
    print "<h1 id = 'one'><center>Your cart is empty! What are you waiting for? Go shopping!</center></h1>"
    print "</div>"
    print "</body>"
    print "</html>"

counter=0
item_list = map(int, itemId)
x=len(item_list)
quant= map(int, quan)
while (counter < x):
    item=item_list[counter]
    counter2=(counter) 
    quantity=quant[counter2]
    counter=counter + 1

    sql2 = "SELECT * FROM inventory_t where item_id = '%s'"%(item)

    try:
        myCursor.execute(sql2)
        output = myCursor.fetchall()
        if (counter == 1):
            print "<h1 id = 'one'><center> Cart Page</center></h1>"
            print "<div id='viewLay'>"
        for row in output:
            print "<form method = 'post' action='removeItem.cgi'>"
            print "<input type='hidden' name = 'itemId' value='%s'>"%(row[0])
            print "<p><img src ='%s' width='200' height='200'></p>" %(row[7])
            print "<p>Item: %s</p>" %(row[6])
            print "<p>Price: %s</p>" %(row[2])
            print "<p>Size: %s</p>" %(row[3])
            print "<p>Quantity: %s"%(quantity)
            print "<input type='number' name='quantity' min='1' max='%s'  value='1'>"%(quantity)
            print "<input type='submit' name='removeI' value='Remove Item'>"
            print "</form><br><br>"
    except:
        print "Error: unable to fetch dataa"
db.close()

if (len(itemId) != 0):
    print "<form method = 'post' action='checkout.cgi'>"
    print "<center><input type='submit' name='checkout' value='Checkout'></center>"
else:
    print "<form method = 'post' action='catalog.cgi'>"
    print "<p><center><input type='submit' name='shop' value='Shop'></center></p>"
print "</form>"
print "</div>"    
print "</body>"
print "</html>"
