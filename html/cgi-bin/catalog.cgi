#!/usr/bin/python
import cgi, cgitb
import MySQLdb
from dbInfo import *

db,myCursor = dbConnectCursor()

sql = "SELECT * FROM inventory_t;"

try:
        myCursor.execute(sql)
        output = myCursor.fetchall()
        print "Content-type:text/html\r\n\r\n"
        print "<html>"
        print "<head>"
        print "<title> Catalog</title>"
        print "<link href='https://fonts.googleapis.com/css?family=Merienda' rel='stylesheet'>"
        print "<link rel='stylesheet' href='../catKittyFormat.css' />"
        print "<head>"
        print "<body>"
        print "<h2 id = 'one'><center> Check out these cool items!</center></h2>"
       
        for row in output:
                print "<form method = 'post' action='view_item.cgi'>"
                print "<input type='hidden' name = 'itemId' value='%s'>"%(row[0])
                print "<p><img src ='%s' width='200' height='300'>" %(row[7])
                print "Price: %s" %(row[2])
                print "Item: %s" %(row[6])
                print "<input type='submit' name='item' value='View Item'>"
                print "</form>"
                print "</p>"       
        print "</body>"
        print "</html>"        
except:
        print "Error: unable to fetch data"
db.close()
