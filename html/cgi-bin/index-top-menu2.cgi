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
          <li><a class="active" href="../index.html" onClick="window.location.href='index-top-menu2.cgi'">Home</a></li>
          <li><a href="../about.htm" onClick="window.location.href='index-top-menu2.cgi'">About</a></li>
          <li><a href="logout.cgi" target="BOT">Logout</a></li>
          <li><a href="catalog.cgi" target="BOT" onClick="window.location.href='index-top-menu2.cgi'">Shop</a></li>
          <li><a href="cart.cgi" target="BOT" onClick="window.location.href='index-top-menu2.cgi'">Cart</a></li-last>
        </ul>
        
        <div id = "main">

          <h3 id = "header">You'll Never Want to Own Another Piece of Clothing</h3>

        <div id = "pics"><center><img src="../HarryShirt.jpeg" width="300" height="400"> <p><id = "quotes"> 
          "I saw him and knew I needed him in my life...on a shirt." <br>- Satisfied Customer</id></p></center></div>

        <div id = "pics"><center><img src="../jerrysock.jpeg" width="300" height="400"><p><id = "quotes">
          "Cutest socks ever. I stared at these socks for 2 weeks straight. I don't know how I lived without these." <br>- Very Satisfied Customer </id>
        </center></div>

        <div id = "pics"><center><img src="../earltank.jpeg" width="300" height="400"><p><id = "quotes">
          "This is the only shirt I own now. I bought 20 of the tank with Earl on it. I threw everything else out. My life is complete." <br>
          - Extremely Satisfied Customer (maybe stay away from them)</id></p></center></div>

        <center><strong>Be as satisfied as these customers. Start Shopping Now!</strong></center>
        <p id = "spacing"> </p>
       </div>

        """
    except KeyError:
        print """
        <div id = "header",class="header">
        <h1>The Kitty Cabin</h1>
        <br>Clothes for the Ultimate Cat Lover
        </div>

        <ul>
          <li><a class="active" href="../index.html" onClick="window.location.href='index-top-menu2.cgi'">Home</a></li>
          <li><a href="../about.htm">About</a></li>
          <li><a href="../login.htm">Login</a></li>
          <li><a href="../register.htm">Register</a></li>
          <li><a href="catalog.cgi" onClick="window.location.href='index-top-menu2.cgi'">Shop</a></li>
          <li><a href="cart.cgi" onClick="window.location.href='index-top-menu2.cgi'">Cart</a></li-last>
        </ul>    
        
        <div id = "main">

          <h3 id = "header">You'll Never Want to Own Another Piece of Clothing</h3>

        <div id = "pics"><center><img src="../HarryShirt.jpeg" width="300" height="400"> <p><id = "quotes"> 
          "I saw him and knew I needed him in my life...on a shirt." <br>- Satisfied Customer</id></p></center></div>

        <div id = "pics"><center><img src="../jerrysock.jpeg" width="300" height="400"><p><id = "quotes">
          "Cutest socks ever. I stared at these socks for 2 weeks straight. I don't know how I lived without these." <br>- Very Satisfied Customer </id>
        </center></div>

        <div id = "pics"><center><img src="../earltank.jpeg" width="300" height="400"><p><id = "quotes">
          "This is the only shirt I own now. I bought 20 of the tank with Earl on it. I threw everything else out. My life is complete." <br>
          - Extremely Satisfied Customer (maybe stay away from them)</id></p></center></div>

        <center><strong>Be as satisfied as these customers. Start Shopping Now!</strong></center>
        <p id = "spacing"> </p>
       </div>
        """    
       
else: 
    print """
    <div id = "header",class="header">
    <h1>The Kitty Cabin</h1>
    <br>Clothes for the Ultimate Cat Lover
    </div>

    <ul>
      <li><a href="../index.html" onClick="window.location.href='index-top-menu2.cgi'">Home</a></li>
      <li><a href="../about.htm">About</a></li>
      <li><a href="../login.htm" target="BOT">Login</a></li>
      <li><a href="../register.htm" target="BOT">Register</a></li>
      <li><a href="catalog.cgi" target="BOT" onClick="window.location.href='index-top-menu2.cgi'">Shop</a></li>
      <li><a href="cart.cgi" target="BOT" onClick="window.location.href='index-top-menu2.cgi'">Cart</a></li-last>
    </ul>
    
    <div id = "main">

          <h3 id = "header">You'll Never Want to Own Another Piece of Clothing</h3>

        <div id = "pics"><center><img src="../HarryShirt.jpeg" width="300" height="400"> <p><id = "quotes"> 
          "I saw him and knew I needed him in my life...on a shirt." <br>- Satisfied Customer</id></p></center></div>

        <div id = "pics"><center><img src="../jerrysock.jpeg" width="300" height="400"><p><id = "quotes">
          "Cutest socks ever. I stared at these socks for 2 weeks straight. I don't know how I lived without these." <br>- Very Satisfied Customer </id>
        </center></div>

        <div id = "pics"><center><img src="../earltank.jpeg" width="300" height="400"><p><id = "quotes">
          "This is the only shirt I own now. I bought 20 of the tank with Earl on it. I threw everything else out. My life is complete." <br>
          - Extremely Satisfied Customer (maybe stay away from them)</id></p></center></div>

        <center><strong>Be as satisfied as these customers. Start Shopping Now!</strong></center>
        <p id = "spacing"> </p>
    </div>
    """
print """
</body>
</html>

"""
