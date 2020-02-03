#!/usr/bin/python
import cgi, cgitb
import MySQLdb
import Cookie
import os
from dbInfo import *

myForm = cgi.FieldStorage()
print "Content-type:text/html\n\n"
print """
<html>
<head>

        <title>Registration | The Kitty Cabin</title>
        <link href='https://fonts.googleapis.com/css?family=Merienda' rel='stylesheet'>
        <link rel="stylesheet" href="../topKittyFormat2.css" />
        <link rel="stylesheet" href="../regKittyFormat.css" />
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
          <li><a class="active" href="register2.cgi">Register</a></li>
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
      <li><a class="active" href="register2.cgi">Register</a></li>
      <li><a href="catalog.cgi">Shop</a></li>
      <li><a href="cart.cgi">Cart</a></li-last>
    </ul>
    </nav>
    """
    
print """
<script>
  function hideInd(x) {
    if(x.checked) {
      document.getElementById("I").style.display = "none";
      document.getElementById("B").style.display = "initial";
      document.getElementById("S").style.display = "none";  
    }
  }

  function hideBus(x) {
    if(x.checked) {
      document.getElementById("B").style.display = "none";
      document.getElementById("I").style.display = "initial";
      document.getElementById("S").style.display = "none";
    }
  }
  function hideStaf(x) {
    if(x.checked) {
      document.getElementById("B").style.display = "none";
      document.getElementById("S").style.display = "initial";
      document.getElementById("I").style.display = "none";
    }
  }
</script>

<div id="regLay">
<input type="radio" onload="hideInd(this)" onclick="hideInd(this)" name="custType" value="Business" checked> Business 
<input type="radio" onclick="hideBus(this)" name="custType" value="Individual"> Individual
<!-- <input type="radio" onclick="hideStaf(this)" name="custType" value="Staff"> Staff -->
<h2> Registration </h2>
  <div id = "B">
    <form method="post" action="register.cgi">
    <div id ="one"> 
                Full Name:<br>
                <input type="hidden" name="custType" value="Business">
                <input type="text" name="custName"><br>
                Business Email:<br>
                <input type="text" name="custEmail"><br>
                Password:<br>
                <input type="text" name="custPassword"><br>
                Confirm Password:<br>
                <input type="text" name="confirmPassword"><br>
                Shipping Address:<br>
                <input type="text" name="address"><br>
                Bank Account Number:<br>
                <input type="text" name="debitCardNum"><br>
                <p><input type="submit" value="Submit"></p>
</div>
</form></div>

<div id = "I" style="display: none;"> 
  <form method="post" action="register.cgi">
  <div id ="one"> 
                Full Name:<br>
                <input type="hidden" name="custType" value="Individual">
                <input type="text" name="custName"><br>
                Email:<br>
                <input type="text" name="custEmail"><br>
                Password:<br>
                <input type="text" name="custPassword"><br>
                Confirm Password:<br>
                <input type="text" name="confirmPassword"><br>
                Address:<br>
                <input type="text" name="address">
                <p><input type="submit" value="Submit"></p>
  </div>
  </form></div>

  <div id = "S" style="display: none;> 
  <form method="post" action="register.cgi">
  <div id ="one"> 
                Full Name:<br>
                <input type="hidden" name="custType" value="Staff">
                <input type="text" name="custName"><br>
                Email:<br>
                <input type="text" name="custEmail"><br>
                Password:<br>
                <input type="text" name="custPassword"><br>
                Confirm Password:<br>
                <input type="text" name="confirmPassword"><br>
                <p><input type="submit" value="Submit"></p>
  </div>
  </form></div>
</div>  
"""
