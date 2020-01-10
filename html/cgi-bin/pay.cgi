#!/usr/bin/python
import cgi, cgitb
import MySQLdb
import Cookie
import os
import subprocess
from dbInfo import *

myForm = cgi.FieldStorage()

item = myForm.getvalue('itemId') 
total = myForm.getvalue('totalAm')
bankN = myForm.getvalue('bankNum')
shipMethod = myForm.getvalue('sMethod')

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
print "<div id=viewLay>"
print "<h2 id='one'><center>Confirmation Page</center></h2>"

sql = "SELECT * FROM customer_t WHERE customer_id = '%s'"%(cData)

try:
        myCursor.execute(sql)
        output = myCursor.fetchall()
        for row in output:
                custId = row[0]
                custPass = row[1]
                sAdd = row[5]
                dCard = row[6]        
except:
        print "error: could not fetch data"     

sql2 = "SELECT * FROM cart WHERE customer_id = '%s' AND quantity > 0"%(cData)

try:
        myCursor.execute(sql2)
        output = myCursor.fetchall()
        itemId=[]
        quan=[]
        for row in output:
            itemId.append(row[2])
            quan.append(row[3])    
except:
        print "Error: unable to fetch data"

# Place item information in arrays to access later: 
payee = 888888 ##my bank id
counter=0
item_list = map(int, itemId)
x=len(item_list)
quant= map(int, quan)
quan2 =1
tprice=[]
curQuan=[]
tIn=[]
tSold=[]

while (counter < x):
    item=item_list[counter]
    counter2=(counter) 
    quantity=quant[counter2]
    counter=counter + 1

    sql6 = "SELECT * FROM inventory_t WHERE item_id = '%s'"%(item)

    try:    
        myCursor.execute(sql6)
        output = myCursor.fetchall()
        for row in output:
            tprice.append(row[2])
            curQuan.append(row[1])
            tIn.append(row[4])
            tSold.append(row[5])
    except:
        print "Error fetching data"    

tPrice = map(float, tprice)
curQuan=map(int, curQuan)
tIn=map(int, tIn)
tSold=map(int,tSold)

# Connecting to Shipping Company: 
counter2=0
while(counter2 < x):
    counter2 = counter2 + 1  
    
    shipInfo = str(custId) + " " + str(custPass) + " " + str(item) + " " + shipMethod + " " + sAdd
    shipFile = open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/Q-ship.txt", "w")
    shipFile.write(shipInfo)
    shipFile.close()
  
    #changing port:
    changePort = open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/necPorts.txt", "w")
    changePort.write("11194 11195 /var/www/ebusiness/b-f19-06/html/files/ClientSocket/f-Q-ship.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/Q-ship.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/Qs.dat /var/www/ebusiness/b-f19-06/html/files/ClientSocket/f-A-ship.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/A-ship.txt As.dat") #/var/www/ebusiness/b-f19-06/html/files/ClientSocket/As.dat
    changePort.close()
    
    #calling Client     
    p1 = subprocess.Popen(["/usr/bin/java", "Client"], stdout=subprocess.PIPE)
    print p1.stdout.read()
    
    with open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/A-ship.txt", "r") as file:
        shipRes=file.readline() #file.read()
        shipConf=file.readline()
    shipConf = str(shipConf)    
    shipRes=map(str,shipRes)
    shipRes2=shipRes[0]
    
    sql3 = "INSERT INTO ShippingRequest_t (CustomerID, Password, CRequestID, ItemIDOrdered, ShipMethod, ShipAddress) VALUES ('%s', '%s', '%s', %s, '%s', '%s')"%(custId, custPass, shipConf, item, shipMethod, sAdd)

    try:
        myCursor.execute(sql3)  
    except:
        db.rollback()
    
    transShip = False
    if(shipRes2 == "0"):
        transShip = True
    else:
         print "Something wrong with Ship Request"    

#updating order_t:    
counter2=0
while(counter2 < x):
    counter2=counter2 + 1       
    sql4 = "INSERT INTO order_t (customer_id, item_id_ordered, quantity, ship_method, ship_address, debit_card_num) VALUES (%s, %s, %s, '%s', '%s', '%s')"%(custId, item, quantity, shipMethod, sAdd, dCard)

    try:
        myCursor.execute(sql4)
    except:
        print("something wrong")
        db.rollback()    

# Conncecting to Bank:
counter2=0
while(counter2 < x):
    totPrice=tPrice[counter2]
    counter2=counter2+1
    
    bankInfo = custPass + " " + str(custId) + " " + str(payee) + " " + str(bankN) + " " + str(totPrice)
    print(bankInfo)    
    bankFile = open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/Q-bank.txt", "w")
    bankFile.write(bankInfo)
    bankFile.close()
    
    #changing ports and files:
    changePort = open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/necPorts.txt", "w")
    changePort.write("11198 11199 /var/www/ebusiness/b-f19-06/html/files/ClientSocket/f-Q-bank.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/Q-bank.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/Qs.dat /var/www/ebusiness/b-f19-06/html/files/ClientSocket/f-A-bank.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/A-bank.txt As.dat") #/var/www/ebusiness/b-f19-06/html/files/ClientSocket/As.dat
    changePort.close()
    
    #calling Client
    p1 = subprocess.Popen(["/usr/bin/java", "Client"], stdout=subprocess.PIPE)
    print p1.stdout.read()
    with open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/A-bank.txt", "r") as file:
        bankRes=file.readline()  #file.read()
        bankConf=file.readline()
    bankConf = str(bankConf)    
    bankRes=map(str,bankRes)
    bankRes2=bankRes[0]
   
    sql5 = "INSERT INTO BankRequest_t (CustomerID, Password, CRequestID, PayeeAccount, PayorAccount, Amount) VALUES ('%s', '%s', '%s', %s, %s, %s)"%(custId, custPass, bankConf, payee, bankN, totPrice)
   
    try:
        myCursor.execute(sql5)
    except:
        db.rollback()    
    
    transBank = False    
    if(bankRes2 == "0"):
        transBank = True
    else:
        print "Something wrong with Bank Request"

# Connecting to Mayor/Tax:
counter2=0
taxAcc=7654321
taxPass="dcba"
while(counter2 < x):
    totPrice=tPrice[counter2]
    counter2 = counter2 + 1  

    mayorInfo = str(totPrice) + " " + str(bankN) + " " + str(taxAcc) + " " + taxPass
    mayorFile = open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/Q-mayor.txt", "w")
    mayorFile.write(mayorInfo)
    mayorFile.close()

    #changing port:
    changePort = open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/necPorts.txt", "w")
    changePort.write("11196 11197 /var/www/ebusiness/b-f19-06/html/files/ClientSocket/f-Q-mayor.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/Q-mayor.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/Qs.dat /var/www/ebusiness/b-f19-06/html/files/ClientSocket/f-A-mayor.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/A-mayor.txt As.dat")

    changePort.close()
    
    #calling Client     
    p1 = subprocess.Popen(["/usr/bin/java", "Client"], stdout=subprocess.PIPE)
    print p1.stdout.read()
    
    with open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/A-mayor.txt", "r") as file:
        mayorRes=file.readline() #file.read()
        mayorConf=file.readline()
    mayorConf = str(mayorConf)
    mayorRes=map(str,mayorRes)
    mayorRes2=mayorRes[0]

    sqlMayor = "INSERT INTO TaxRequest_t (CRequestID, Amount, BankAccount, TaxAccount, TaxPassword) VALUES ('%s', %s, %s, %s, '%s')"%(mayorConf, totPrice, bankN, taxAcc, taxPass)

    try:
        myCursor.execute(sqlMayor)  
    except:
        db.rollback()
    
    transMayor = False
    if(mayorRes2 == "0"):
        transMayor = True
    else:
         print "Something wrong with Mayor/Tax Request"        

# Connecting to IT Services:
counter2=0
itAcc=1234567
itPass="abcd"
while(counter2 < x):
    totPrice=tPrice[counter2]
    counter2 = counter2 + 1  
    
    itInfo = str(item) + " " + str(quantity) + " " + str(totPrice) + " " + str(bankN) + " " + shipMethod + " " + sAdd + " " + str(itAcc) + " " + itPass
    itFile = open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/Q-it.txt", "w")
    itFile.write(itInfo)
    itFile.close()

    #changing port:
    changePort = open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/necPorts.txt", "w")
    changePort.write("11198 11199 /var/www/ebusiness/b-f19-06/html/files/ClientSocket/f-Q-it.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/Q-it.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/Qs.dat /var/www/ebusiness/b-f19-06/html/files/ClientSocket/f-A-it.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/A-it.txt As.dat")
    changePort.close()
    
    #calling Client     
    p1 = subprocess.Popen(["/usr/bin/java", "Client"], stdout=subprocess.PIPE)
    print p1.stdout.read()
    
    with open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/A-it.txt", "r") as file:
        itRes=file.readline() #file.read()
        itConf=file.readline() 
    itConf = str(itConf)
    itRes=map(str,itRes)
    itRes2=itRes[0]

    sqlIT = "INSERT INTO ITRequest_t (CRequestID, ItemID, Quantity, SaleAmount, BankAccount, ShipMethod, ShipAddress, ITAccount, ITPassword) VALUES ('%s', %s, %s, %s, %s, '%s', '%s', %s, '%s')"%(itConf, item, quantity, totPrice, bankN, shipMethod, sAdd, itAcc, itPass)

    try:
        myCursor.execute(sqlIT)  
    except:
        db.rollback()
    
    transIt = False
    if(itRes2 == "0"):
        transIt = True
    else:
         print "Something wrong with IT Services Request"

#Update Inventory Table:               
counter2=0        
while(counter2 < x):
    item=item_list[counter2]
    totPrice=tPrice[counter2]
    curQuant=curQuan[counter2]-quantity
    totIn=tIn[counter2]-quantity
    totSold=tSold[counter2]+quantity 
    counter2 = counter2 + 1
    
    sql7 = "UPDATE inventory_t SET current_quantity=%s, total_in=%s, total_sold=%s WHERE item_id=%s"%(curQuant,totIn,totSold,item)       
    
    try:
        myCursor.execute(sql7)
    except:
        db.rollback()

#Update/remove row in cart table after successful order:
sqldC = "DELETE FROM cart WHERE customer_id = '%s'"%(custId)  
        
print(transBank)        
if transBank != True:
    print "<h3 id='one'><center>Issue with Bank Transaction. Please try again.</h3></center>"
if transShip != True:
    print "<h3 id='one'><center>Issue with Ship Transaction. Please try again.</h3></center>"
else:
    db.commit()
    try:
        myCursor.execute(sqldC)
        db.commit()
    except:
        db.rollback()
    print "<h3 id ='one'><center>SUCCESS! Thank You for your order!</center></h3>"

    sqlOrder = "SELECT MAX(order_id) FROM order_t WHERE customer_id = '%s'"%(custId) #"SELECT MAX(order_id) FROM order_t WHERE customer_id ='%s'"%(custId)

    try:
        myCursor.execute(sqlOrder)
        output = myCursor.fetchone()
        for row in output:
            orderId = row
        orderConf = "1200" + str(orderId)    
        print "<center>Your Order Number is: %s</center>"%(orderConf)     
    except:
        print "Error Fetching data"          
    
    sqlConf = "UPDATE order_t SET order_conf = %s WHERE order_id = %s"%(orderConf, orderId)
    
    try:
        myCursor.execute(sqlConf)
        db.commit()
    except:
        print "Error updating Order Table with Confirmation Number"
        db.rollback()    
print "</div>"
print "</body>"
print "</html>"
db.close()
