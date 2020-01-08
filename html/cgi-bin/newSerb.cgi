#!/usr/bin/python
import cgi, cgitb
import MySQLdb
import Cookie
import os
import subprocess
from dbInfo import *

print "Content-type:text/html\n\n"

##read the file
with open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/Qs.dat", "r") as file:
        custQues=file.read()
        custQues=str(custQues)
##iterate through the words in the string
cusQuest = custQues.split(" ")
custId = cusQuest[0]
custPass = cusQuest[1]
itemId = cusQuest[2]
quant = cusQuest[3]
sMethod = cusQuest[4]

db,myCursor = dbConnectCursor()                

sql = "SELECT * FROM customer_t WHERE customer_id = '%s'"%(custId)

answer = "0"

try:
    myCursor.execute(sql)
    output = myCursor.fetchall()
    for row in output:
        custId = row[0]
        custPass = row[1]
        custType = row[4]
        sAdd = row[5]
        dCard = row[6] #This will be bank account
except:
    answer = "1"
    print "Account does not exist"

if (custType != "Business"):
    answer = "2"
    print "Wrong account type, try again with a BUSINESS account."        
        
payee = 888888 #change to what bank account number is

sql2 = "SELECT * FROM inventory_t WHERE item_id = '%s'"%(itemId)

try:
    myCursor.execute(sql2)
    output = myCursor.fetchall()
    for row in output:
        tprice=row[2]
        curQuan=row[1]
        tIn=row[4]
        tSold=row[5]
except:
    print "Error fetching data"        

## Connecting to Shipping Company:    

shipInfo = str(custId) + " " + str(custPass) + " " + str(itemId) + " " + str(sMethod) + " " + str(sAdd)
shipFile = open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/Q-ship.dat", "w")
shipFile.write(shipInfo)
shipFile.close()

#changing port:
changePort = open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/necPorts.txt", "w")
changePort.write("11194 11195 /var/www/ebusiness/b-f19-06/html/files/ClientSocket/f-Q-ship.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/Q-ship.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/Qs.dat /var/www/ebusiness/b-f19-06/html/files/ClientSocket/f-A-ship.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/A-ship.txt As.dat")
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

print("Confimation:")
print(shipConf)

sql3 = "INSERT INTO ShippingRequest_t (CustomerID, Password, CRequestID, ItemIDOrdered, ShipMethod, ShipAddress) VALUES ('%s', '%s', '%s', %s, '%s', '%s')"%(custId, custPass, shipConf, itemId, sMethod, sAdd)

try:
    myCursor.execute(sql3)  
except:
    db.rollback()
    
transShip = False   #maybe alter to only have answer
if(shipRes2 == "0"):
    transShip = True
else:
    answer = "3"
    print "Something wrong with Ship Request"

##Add Order to order_t:

sql5 = "INSERT INTO order_t (customer_id, item_id_ordered, quantity, ship_method, ship_address, debit_card_num) VALUES (%s, %s, %s, '%s', '%s', %s)"%(custId, itemId, quant, sMethod, sAdd, dCard) 

try:
    myCursor.execute(sql5)
except:
    db.rollback()

tprice2 = tprice * int(quant)

## Connecting to Bank Company:

bankInfo = custPass + " " + str(custId) + " " + str(payee) + " " + str(dCard) + " " + str(tprice2)
print(bankInfo)
bankFile = open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/Q-ship.dat", "w")
bankFile.write(bankInfo)
bankFile.close()

#changing ports and files:
changePort = open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/necPorts.txt", "w")
changePort.write("11198 11199 /var/www/ebusiness/b-f19-06/html/files/ClientSocket/f-Q-bank.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/Q-bank.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/Qs.dat /var/www/ebusiness/b-f19-06/html/files/ClientSocket/f-A-bank.txt /var/www/ebusiness/b-f19-06/html/files/ClientSocket/A-bank.txt As.dat")
changePort.close()

#calling Client
p1 = subprocess.Popen(["/usr/bin/java", "Client"], stdout=subprocess.PIPE)
print p1.stdout.read()
with open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/A-bank.txt", "r") as file:
    bankRes=file.readline()
    bankConf=file.readline()
bankConf = str(bankConf)    
bankRes=map(str,bankRes)
bankRes2=bankRes[0]

sql7 = "INSERT INTO BankRequest_t (CustomerID, Password, CRequestID, PayeeAccount, PayorAccount, Amount) VALUES ('%s', '%s', '%s', %s, %s, %s)"%(custId, custPass, bankConf, payee, dCard, tprice2)

try:
    myCursor.execute(sql7)
except:
    db.rollback()    

transBank = False
if(bankRes2 == "0"):
    transBank = True
else:
    answer = "4"
    print "Something wrong with Bank Request"                         

# Connecting to Mayor/Tax:

taxAcc=7654321
taxPass="dcba"

mayorInfo = str(tprice2) + " " + str(dCard) + " " + str(taxAcc) + " " + taxPass
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
    mayorRes=file.readline() 
    mayorConf=file.readline()
mayorConf = str(mayorConf)
mayorRes=map(str,mayorRes)
mayorRes2=mayorRes[0]

sqlMayor = "INSERT INTO TaxRequest_t (CRequestID, Amount, BankAccount, TaxAccount, TaxPassword) VALUES ('%s', %s, %s, %s, '%s')"%(mayorConf, tprice2, dCard, taxAcc, taxPass)

try:
    myCursor.execute(sqlMayor)  
except:
    db.rollback()

transMayor = False
if(mayorRes2 == "0"):
    transMayor = True
else:
    answer = "5"
    print "Something wrong with Mayor/Tax Request"        

# Connecting to IT Services:

itAcc=1234567
itPass="abcd"  
    
itInfo = str(itemId) + " " + str(quant) + " " + str(tprice2) + " " + str(dCard) + " " + sMethod + " " + sAdd + " " + str(itAcc) + " " + itPass
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

sqlIT = "INSERT INTO ITRequest_t (CRequestID, ItemID, Quantity, SaleAmount, BankAccount, ShipMethod, ShipAddress, ITAccount, ITPassword) VALUES ('%s', %s, %s, %s, %s, '%s', '%s', %s, '%s')"%(itConf, itemId, quant, tprice2, dCard, sMethod, sAdd, itAcc, itPass)

try:
    myCursor.execute(sqlIT)  
except:
    db.rollback()
    
transIt = False
if(itRes2 == "0"):
    transIt = True
else:
    answer = "6"
    print "Something wrong with IT Services Request"

##UPDATING inventory_t:         

sql8 = "UPDATE inventory_t SET current_quantity=%s, total_in=%s, total_sold=%s WHERE item_id=%s"%(curQuan,tIn,tSold,itemId)

try:
    myCursor.execute(sql8)
except:
    db.rollback()
        
if transBank != True:
    print "Issue with Bank Transaction. Please try again."
elif transShip != True:
    print "Issue with Ship Transaction. Please try again."
elif transMayor != True:
    print "Issue with Mayor Transaction. Please try again."
elif transIt != True:
    print "Issue with IT Services Transaction. Please try again."

if (answer != "0"):
    print "Something wrong with Transaction"    
else:   
    db.commit()
    
    sqlOrder = "SELECT MAX(order_id) FROM order_t WHERE customer_id ='%s'"%(custId)

    try:
        myCursor.execute(sqlOrder)
        output = myCursor.fetchone()
        for row in output:
            orderId = row
        orderConf = "1210" + str(orderId)    
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
db.close()

B2BAc = open("/var/www/ebusiness/b-f19-06/html/files/ClientSocket/As.dat", "w") 
B2BAc.write(str(answer) + "\n" + orderConf)
B2BAc.close()
