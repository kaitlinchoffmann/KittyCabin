#!/usr/bin/python
import cgi, cgitb
import MySQLdb
from dbInfo import *

webForm = cgi.FieldStorage()

custName = webForm.getvalue('custName')
custEmail = webForm.getvalue('custEmail')
custPass = webForm.getvalue('custPassword')
conPass = webForm.getvalue('confirmPassword')
address = webForm.getvalue('address')
debitNum = webForm.getvalue('debitCardNum')
custType = webForm.getvalue('custType')

print "Content-type:text/html\r\n\r\n"
 
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
if len(cId) > 0:
    print ("Email already registered, login or register with different email!")
elif (custPass != conPass):
    print("Password confirmation must be same as password.")
elif((custType == "Business") and (custName is None or custEmail is None or custPass is None or conPass is None or address is None or custType is None or debitNum is None)):
        print("Cannot leave anything blank. Please complete entire form.")      
elif ((custType == "Individual") and (custName is None or custEmail is None or custPass is None or conPass is None or address is None or custType is None)):
        print("Cannot leave anything blank. Please complete entire form.")
elif ((custType == "Individual") and (custName is None or custEmail is None or custPass is None or conPass is None or custType is None)):
        print("Cannot leave anything blank. Please complete entire form.")            
else:
  try:
      myCursor.execute(sql)
      db.commit()
      conti=True
      print "<html>"
      print "<head>"
      print "<link rel='stylesheet' href='../kittyformat.css' />"
      print "<title> REGISTRATION FORM</title>"
      print "</head>"
      print "<body>"
      print "<h2 id = 'one'><center> Congratulations! You Have Successfully Registered %s!</center> </h2>" %(custName)
      print "<h3><center> Please login to start shopping:</center> "
      print "<form method = 'post' action='../login.htm'>"
      print "<input type='hidden' name='cusType' value='custType'>"
      print "<center><input type='submit' name='login' value='Login'></center>"
      print "</form>"
      print "</body>"
      print "</html>"
  except:
      db.rollback()                   
db.close()
