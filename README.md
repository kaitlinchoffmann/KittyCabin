# KittyCabin
E-Business Project

1. Developer Guide

1.1 URL to The Kitty Cabin

https://cs.newpaltz.edu/e/b-f19-06/cgi-bin/

1.2 What is The Kitty Cabin?

The Kitty Cabin is an E-Business created for my E-Business Systems graduate course. The Client Side of this system uses HTML, CSS, and JavaScript while the Server Side uses Python and Common Gateway Interface (CGI) to make The Kitty Cabin dynamic. MySQL is the datebase used. To get an in-depth analysis on the creation of The Kitty Cabin, please refer to the "12-FinalReport.pdf" under the "kaitlinchoffmann/KittyCabin" repository. Users can "shop" for clothes that have pictures of my lovely cats on them. The Kitty Cabin is NOT a real E-Business and was created strictly for educational purposes so you cannot actually buy these items. Please DO NOT input any identifiable or "real" information when signing up as a user on The Kitty Cabin. Example, do not put your real home address or your real credit card number. This website is not entirely secure, however, my goal is to continue to improve this website as I learn more in my program. 

1.3 How to Run/Setup The Kitty Cabin

Files can be used as a template for your own website, however, you will have to create your own database to retain user information. Cookies and Common Gateway Interface (CGI) are used to make the website dynamic. AGAIN, please DO NOT input any identifiable or "real" information when signing up as a user on The Kitty Cabin.

The Kitty Cabin uses socket programs to connect to other companies which were provided by Dr. Hanh Pham. These programs are written in Java and are called Server.java and Client.java. The Server.java program is The Kitty Cabin's way to answer connections from other companies if they want to purchase items from The Kitty Cabin. The Client.java program is the way The Kitty Cabin connects to other companies, such as the shipping company and bank. Port connections called from the Client.class to other companies, such as shipping, bank, IT Servies and Mayor, are simply test ports. Basically, these ports are not connections to real businesses. They simply return a 0 and confirmation number on consecutive lines. 

In order for companies to have access to The Kitty Cabin, make sure Server.java is running as a background process by typing "java Server &" in the command line where the Server.java program is located. The Server program can be found under sockets folder: html/cgi-bin/sockets.
To check if The Kitty Cabin server is still running, enter top in Linux command line to see what is running. To end/kill the server background process, enter top, find the pid, and enter kill pidNumber. 

Example:
If pid is 3047, enter kill 3047 to end the process. 

When sending an order to The Kitty Cabin, directions can be found after registering and logging in as a Business account. When connecting to The Kitty Cabin Server, business’s Client program should change their port to send data to 11120. To get a reply back from the server, change reply port to 11121. Client program’s answer file it is asking for should be /var/www/ebusiness/b-f19-06/html/files/ClientSocket/As.dat. The question file it is sending over to the server is /var/www/ebusiness/b-f19-06/html/files/ClientSocket/Qs.dat. 

Please refer back to chapters 6 and 7 in the Final Report on how to use and access all features of The Kitty Cabin if needed.

1.4 Issues to Look Out For

If ports to the Bank, Shipping Company, Mayor, and/IT Services are closed, transactions can not be done successfully. In this case, error messages should indicate where the issue is coming from. The ports used are test ports provided by Dr. Hanh Pham. Sometimes connection to The Kitty Cabin server will also be down. Any issues with the ports or the server connection to the Kitty Cabin, please contact the email under the About page for assistance in this matter.   

1.5 Changes Needed When Moving Folders

CGI programs, pay.cgi, newSerb.cgi, and b2b.cgi have in them where to look for flag files and question and answer files. These are located under the ClientSocket folder under the files folder, html/files/ClientSocket. If any of these files were to move, these changes must be reflected under pay.cgi, newSerb.cgi and b2b.cgi. 

Many HTML files are connecting to other HTML files or cgi programs. Thus, if anything were to move, this must be reflected in all HTML files that are connecting them.
