#!/usr/bin/python
import cgi, cgitb
import MySQLdb
from dbInfo import *
import Cookie
import os

webForm = cgi.FieldStorage()

custName = webForm.getvalue('custName')
custEmail = webForm.getvalue('custEmail')
custPass = webForm.getvalue('custPassword')
conPass = webForm.getvalue('confirmPassword')
address = webForm.getvalue('address')
debitNum = webForm.getvalue('debitCardNum')
custType = webForm.getvalue('custType')

print "Content-type:text/html\r\n\r\n"
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
 
db,myCursor = dbConnectCursor()

customer_id = myCursor.lastrowid
payee=8888

sql = "INSERT INTO customer_t VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(customer_id,custPass,custEmail,custName,custType,address,debitNum)       
sql2 = "SELECT customer_id FROM customer_t WHERE email = '%s'"%(custEmail)
sql3 = "select count(*) AS total from customer_t where email='%s'"%(custEmail)
 
try:    
    myCursor.execute(sql2)
    output = myCursor.fetchall()
    cId=[]
    for row in output:
      cId.append(row[0])    
except:
    print("Unable to fetch data")    

conti=False
if((len(cId) > 0) or (custPass != conPass) or ((custType == "Business") and (custName is None or custEmail is None or custPass is None or conPass is None or address is None or custType is None or debitNum is None)) or ((custType == "Individual") and (custName is None or custEmail is None or custPass is None or conPass is None or address is None or custType is None)) or ((custType == "Individual") and (custName is None or custEmail is None or custPass is None or conPass is None or custType is None))):
    if len(cId) > 0:
        print ("<h3 id = 'one'><center>Email already registered, login or register with different email!</center></h3>")
    elif (custPass != conPass):
        print("<h3 id = 'one'><center>Password confirmation must be same as password.</center></h3>")
    elif((custType == "Business") and (custName is None or custEmail is None or custPass is None or conPass is None or address is None or custType is None or debitNum is None)):
        print("<h3 id = 'one'><center>Cannot leave anything blank. Please complete entire form.</center></h3>")      
    elif ((custType == "Individual") and (custName is None or custEmail is None or custPass is None or conPass is None or address is None or custType is None)):
        print("<h3 id = 'one'><center>Cannot leave anything blank. Please complete entire form.</center></h3>")
    elif ((custType == "Individual") and (custName is None or custEmail is None or custPass is None or conPass is None or custType is None)):
        print("<h3 id = 'one'><center>Cannot leave anything blank. Please complete entire form.</center></h3>")            
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
    <input type="radio" onclick="hideStaf(this)" name="custType" value="Staff"> Staff
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
    <div id = "I"> 
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
      <div id = "S"> 
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
else:
    try:
        myCursor.execute(sql)
        db.commit()
        conti=True
        print "<h2 id = 'one'><center> Congratulations! You Have Successfully Registered %s!</center> </h2>" %(custName)
        print "<h3><center> Please login to start shopping:</center>"
        print "<div id='body2'>"
        print "<center>"
        print "<h2>Login</h2>"  
        print "<form method = 'post' action='login.cgi'>"
        print "<div id ='one'>"		 
        print "<p>Email:" 
        print "<input type='text' name='custEmail'><br>"
        print "Password:"
        print "<input type='text' name='password'><br>"
        print "<input type='submit' value='Sign In' name='Sign In'>"
        print "</p>" 
        print "</div>"                      
        print "</form>"
    except:
        db.rollback()                   
print "</body>"
print "</html>"
db.close()
