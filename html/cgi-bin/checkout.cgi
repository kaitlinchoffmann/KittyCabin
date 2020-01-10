#!/usr/bin/python
import cgi, cgitb
import MySQLdb
import Cookie
import os
from dbInfo import *

myForm = cgi.FieldStorage()

item = myForm.getvalue('itemId') 

db,myCursor = dbConnectCursor()

print "Content-type:text/html\n\n"
print """
<html>
<head>

        <title>The Kitty Cabin</title>
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

sql3 = "SELECT * FROM customer_t WHERE customer_id = '%s'"%(cData)

sql = "SELECT * FROM cart WHERE customer_id = '%s' AND quantity > 0"%(cData)     

print """
<h1 id = 'one'><center>Checkout</center></h1>

<div id= "viewLay">
<h2>1 Shipping Information</h2>
"""
print "<form method = 'post' action='confirmCheck.cgi'>"            

try:
    myCursor.execute(sql3)
    output = myCursor.fetchall()
    for row in output:
        print "<input type='hidden' name = 'cartId' value='%s'>"%(row[0])
        print "<p>Shipping Address: <input type='text' name='shipAddress' value='%s'></p>"%(row[5])
        print "<p>Shipping Method: " 
        print "<input type='radio' name='shipMethod' value='1' checked> 1 Standard"
        print "<input type='radio' name='shipMethod' value='2'> 2 Express</p>"
except:
    print("Error: Can't fetch data!")

print """
<html>
<body>
<h2>2 Payment Information</h2>
"""
try:
    myCursor.execute(sql3)
    output = myCursor.fetchall()
    for row in output:
        print "<input type='hidden' name = 'cartId' value='%s'>"%(row[0])
        print "<p>Bank Account Number: <input type='text' name='bankNum' value=%s></p>"%(row[6]) 
except:
    print("Error: Can't fetch data!")
print """
</body>
</html>
"""

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

counter=0
item_list = map(int, itemId)
x=len(item_list)
quant= map(int, quan)

print "<html>"
print "<head>"
print "<title>Review Page</title>"
print "<head>"
print "<body>"
print "<h2>3  Review Items</h2>"

while (counter < x):
    item=item_list[counter]
    counter2=(counter) 
    quantity=quant[counter2]
    counter=counter + 1
                
    sql2 = "SELECT * FROM inventory_t where item_id = '%s'"%(item)

    try:
        myCursor.execute(sql2)
        output = myCursor.fetchall()
        for row in output:
            print "<input type='hidden' name = 'itemId' value='%s'>"%(row[0])
            print "<p><img src ='%s' width = '100' height = '100'>" %(row[7])
            print "%s" %(row[6])
            print "Price: %s" %(row[2])
            print "Size: %s" %(row[3])
            print "Quantity: %s"%(quantity)
    except:
        print("Unable to fetch data")            

print "<center><input type='submit' name='reviewOrder' value='Review Order'></center>"
print "</form>"
print "</div>"
print "</body>"
print "</html>"

db.close()
