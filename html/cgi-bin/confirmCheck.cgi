#!/usr/bin/python
import Cookie
import cgi, cgitb
import MySQLdb
import os
from dbInfo import *

myForm = cgi.FieldStorage()

sAddress = myForm.getvalue("shipAddress")
sMethod = myForm.getvalue("shipMethod")
bNum = myForm.getvalue("bankNum")
item = myForm.getvalue("itemId")

db,myCursor = dbConnectCursor()

print "Content-type:text/html\n\n"
print """
<html>
<body>
"""
if 'HTTP_COOKIE' in os.environ:
    cookie_string=os.environ.get('HTTP_COOKIE')
    c=Cookie.SimpleCookie()
    c.load(cookie_string)

    try:
        cData=c["custId"].value
    except KeyError:
        print "No cookie :("
print """
</body>
</html>

"""

sql = "SELECT customer_address FROM customer_t WHERE customer_id ='%s'"%(cData)
sql2 = "SELECT debit_card_num FROM customer_t WHERE customer_id =%s"%(cData)
sql3 = "UPDATE customer_t2 SET customer_address ='%s' WHERE customer_id ='%s'"%(sAddress,cData)
sql4 = "UPDATE customer_t2 SET debit_card_num =%s WHERE customer_id ='%s'"%(bNum,cData)
sql6 = "SELECT * FROM cart WHERE customer_id = '%s' AND quantity > 0"%(cData)
sql7 = "SELECT customer_name FROM customer_t WHERE customer_id = '%s'"%(cData)

try:
        myCursor.execute(sql)
        output = myCursor.fetchone()
        for row in output:
                custAdd = row   
except:
        print "Error: Unable to fetch data."

try:
        if sAddress != custAdd:
                myCursor.execute(sql3)
                db.commit()
                print "Address Updated from '%s' to '%s'"%(custAdd,sAddress)
except:
        db.rollback()

try:
        myCursor.execute(sql2)
        output = myCursor.fetchone()
        for row in output:
            banCard = row
except:
        print "Error: Unable to fetch data."
        
if bNum is not None and banCard is not None:
    if int(bNum) != int(banCard):
        try:
            myCursor.execute(sql4)
            db.commit()
            print "Bank Account Number Updated from '%s' to '%s'"%(banCard,bNum)
        except:
            db.rollback()

try: 
    myCursor.execute(sql7)
    output = myCursor.fetchone()
    for row in output:
        name = row
except:
    print "Error: Unable to fetch data."

print "<html>"
print "<head>"
print "<title>Review Order | The Kitty Cabin</title>"
print "<link href='https://fonts.googleapis.com/css?family=Merienda' rel='stylesheet'>"
print "<link rel='stylesheet' href='../confirmKittyFormat.css'/>"
print "</head>"
print "<body>"
print "<h2 id = 'one'><center>Review Order</center></h2>" 
print "<form method='post' action='pay.cgi'>"
print "<p>Shipping: %s</p>"%(name)
print "<p>%s</p>"%(sAddress)
print "<p>Ship Method: %s</p>"%(sMethod)
print "<input type='hidden' name='sMethod' value='%s'>"%(sMethod)
print "<p>Bank Account: %s</p>"%(bNum)
print "<input type='hidden' name='bankNum' value=%s>"%(bNum)

try:
   myCursor.execute(sql6)
   output = myCursor.fetchall()
   itemId=[]
   quan=[]
   for row in output:
       itemId.append(row[2])
       quan.append(row[3])
except:
        print "Error: unable to fetch data"

total=0
counter=0
item_list = map(int, itemId)
x=len(item_list)
quant= map(int, quan)
print "Items:"
while (counter < x):
     item=item_list[counter]
     counter2=(counter) 
     quantity=quant[counter2]
     counter=counter + 1
     
     sql5 = "SELECT * FROM inventory_t where item_id = '%s'"%(item)
     
     try:
         myCursor.execute(sql5)
         output = myCursor.fetchall()
         for row in output:
             print "<input type='hidden' name = 'itemId' value='%s'>"%(row[0])
             print "<p><img src ='%s' width='100' height='100'>" %(row[7])
             print row[6]
             print "Price: $%s" %(row[2])
             print "Size: %s" %(row[3])
             print "Quantity: %s"%(quantity)
             total2 = row[2] * quantity
             total+=total2
     except:
         print("Unable to fetch data")
                  
print "<input type='hidden' name='totalAm' value=%s>"%(total)
print "<p>Total: $%s"%(total)      
print "<center><input type='submit' name='confirm' value='Place Order'></center>"
print "</form></p>"
print "<form method = 'post' action='cart.cgi'>"
print "<center><input type='submit' name='toCart' value='Back to Cart'></center>"
print "</form>"
print "</body>"
print "</html>"
db.close()
