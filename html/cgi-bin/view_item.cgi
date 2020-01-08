#!/usr/bin/python
import cgi, cgitb
import MySQLdb
from dbInfo import *

webForm = cgi.FieldStorage()

itemId = webForm.getvalue('itemId')

db,myCursor = dbConnectCursor()

sql = "SELECT * FROM inventory_t WHERE item_id = '%s'"%(itemId)
try:
        myCursor.execute(sql)
        output = myCursor.fetchall()
        print "Content-type:text/html\r\n\r\n"
        print "<html>"
        print "<head>"
        print "<title>Item Page</title>"
        print "<link href='https://fonts.googleapis.com/css?family=Merienda' rel='stylesheet'>"
        print "<link rel='stylesheet' href='../kittyformat.css' />"
        print "</head>"
        print "<body>"
        print "<form method = 'post' action='addItem.cgi'>"
        for row in output:
                print "<input type='hidden' name = 'itemId' value='%s'>"%(row[0])
                print "<h2 id = 'one'><center>%s</center></h2>"%(row[6])
                print "<p><center><img src ='%s'></center></p>" %(row[7])
                print "<p>Price: %s</p>" %(row[2])
                print "<p>Size: %s</p>" %(row[3])
                print "<p>Item ID: %s"%(row[0])
                if (row[1] == 0):
                    print "<p><strong>SOLD OUT</strong></p>"
                else:
                    print "<input type='number' name='quantity' min='1' max='20' value='1'>"    
                    print "<input type='submit' onclick='alert('Added To Cart!')' name='addCart' value='Add to Cart'>"
                    print "</p>"   
        print "</form>" 
        print "</body>"
        print "</html>"       
except:
        print "Error: unable to fetch data"
db.close()
