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

        <title>About | The Kitty Cabin</title>
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
          <li><a class="active" href="about.cgi">About</a></li>
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
          <li><a class="active" href="about.cgi">About</a></li>
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
      <li><a class="active" href="about.cgi">About</a></li>
      <li><a href="../login.htm">Login</a></li>
      <li><a href="register2.cgi">Register</a></li>
      <li><a href="catalog.cgi">Shop</a></li>
      <li><a href="cart.cgi">Cart</a></li-last>
    </ul>
    </nav>
    """
print """
<div id = 'body2'>
<center>
<h2 id = 'one'>Who Are We?</h2> 
<p>We're a clothing company with a love for cats...my cats! Have fun with Earl, Jerry, Gigi and Harry and get a cool item with one of their adorable faces on it. </p>
 <p>For businesses who need to order through an API, please register as a "Business" and login with your company email and password. Directions on how to send your order will automatically pop up once you login. For staff who need to order to another business, register as "Staff" and login with your email and password. Follow the link to the B2B form. Fill out the order in the exact order as indicated by the business's instructions. </p>
 <p>Any questions or issues, please contact us at hoffmank4@hawkmail.newpaltz.edu</p>
 <p>Thank you for your business!</p>
 <img src="../IMG_2525.jpeg" width = 500 height = 500>
</div>
</center> 
</body>
</html>

"""
