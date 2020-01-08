//=================== OS-2-Project ============================
// SERVER Site
// + Receive Data (Question) from the Client Site
// + Send Data (Answer) to the Client Site
//===============================================================

import java.net.*;
import java.io.*;

//===============================================================
// * creates instances of InServer and OutServer
//================================================================
public class Server {

   static int Data_Port = 11120;   // to Receive QUESTION from the Client
   static int Reply_Port = 11121;  // to Send ANSWER to the Client
   
  //String QlockFile = "f-Qs.dat";  // Flag-File for writting QUESTION (from CLIENT)
  // String AlockFile = "f-As.dat";  // Flag-File for writting ANSWER(to the CLIENT)
  //String QFile = "/var/www/ebusiness/b-f19-06/html/files/ClientSocket/Qs.dat";  // File for writting QUESTION (from CLIENT)
  //String AFile = "/var/www/ebusiness/b-f19-06/html/files/ClientSocket/As.dat";  // File for writting ANSWER(to the CLIENT)
   

   /*
    * Application entry point
    * @param args - command line arguments
    */
 public static void main (String args[]) throws IOException {

   // To Receive QUESTION "Qc.dat" (as a SERVER) from the Client
   //........................................................
   InServer IP_Server  = new InServer (Data_Port);
   
   // To Send the ANSWER "As.dat" (as a SERVER) to the Client 
   //........................................................
     
   OutServer List_Server  = new OutServer (Reply_Port);
  
   //Process p = Runtime.getRuntime().exec("python /var/www/ebusiness/b-f19-06/html/cgi-bin/testB2BSer.cgi");
   
  }

} // END of the SERVER class


//==================================================================
// * class creates a OutServer socket for SENDING data TO the CLIENT
//==================================================================
class OutServer implements Runnable {

   ServerSocket server = null;      //Instance of ServerSocket
   Socket socket = null;            //The actual socket used for SENDING data

   String fnameSO = "OUTGOING.dat"; // Name of the File (by default) containning O_data at Server
 
   String AlockFile = "/var/www/ebusiness/b-f19-06/html/files/ClientSocket/f-As.dat";     // Flag-File for ANSWER (DATA at Server to send to Client)
   int fAnswer=0;                    // Value of FLAG for the ANSWER read from file

   PrintStream stream = null;       //A PrintStream is used for SENDING data

   DataInputStream inStream = null; //A DataInputStream is used for reading file name
   int thePort;                     //Port number

   Thread thread;                   //A seperate thread is used to wait for a socket accept

   /*
    * constructor starts the thread
    * @param port - the port to listen to
    */
   public OutServer (int port) {
      thePort = port;

      thread = new Thread (this);
      thread.start ();
   }

   /*
    * the thread that waits for socket
    * connections and SENDs data from a FILE to the CLIENT
    */
   public void run () {
 
      // Create a ServerSocket
      //.......................................
      try {
                   server = new ServerSocket (thePort);
         System.out.println ("OPEN a socket for SENDING data TO the CLIENTat port " + thePort);
      }
      catch (Exception e) {
         System.out.println (e);
         System.exit (1);
      }

      while (true) {
         try {
            socket = server.accept ();
            System.out.println ("Connected to port : " + thePort + " WAITING for the Answer ...");
         }
         catch (Exception e) {
            System.out.println (e);
            System.exit (1);
         }
         
         
       // try {
       //     Process p = Runtime.getRuntime().exec("python /var/www/ebusiness/b-f19-06/html/cgi-bin/newSerb.cgi"); //serb.cgi
       //  }
       //  catch (Exception e) {
       //     System.out.println(e);
       //  }  
         
         
         // Accept file name "name" from the Client
         // ( Client tells WHICH FILE it wants to READ )
         //...............................................................
         String name = null;
         try {
            // Prepare a stream for SENDing later
            stream = new PrintStream (socket.getOutputStream ());

            //Get File name from the CLIENT
            inStream = new DataInputStream (socket.getInputStream ());
            name = inStream.readLine ();
            if (name == null) name = fnameSO;
         }
         catch (Exception e) {
            System.out.println (e);
            break;
         }

    // Need to CHECK the LOCK of the ANSWER from the Server if the given file is READY
    //..................................................................................
         while (fAnswer!=1) {
               // Waiting for the ANSWER to be ready
               // Assume DONE (change 0->1 in "f-As.dat")
               fAnswer = ReadFlag(AlockFile);
                  System.out.println ("Flag Value = "+ fAnswer);
         }         
         fAnswer=0; 
         
         // Open the given FILE
         //........................................................
         FileInputStream fs = null;
         try {
            fs = new FileInputStream (name);
         }
         catch (Exception e) {
            System.out.println (e);
            break;
         }

         // Read Data from the given File and SEND it to the "stream"
         // so that it will go to the Client
         //...........................................................
         DataInputStream ds = new DataInputStream (fs);
         while (true) {
            try {
               String s = ds.readLine (); // Read Data from the given File
               if (s == null) break;
               stream.println (s); // SEND it to the "stream"
            }
            catch (IOException e) {
               System.out.println (e);
               break;
            }
         }

         //  Close FILE and close socket
         //.................................................
         try {
            fs.close ();
            System.out.println ("   Reading file " + name + " and SENDING it,done.");
            socket.close ();
            System.out.println ("Connection closed at port : " + thePort);
         }
         catch (IOException e) {
            System.out.println (e);
         }

      }   // end of while
   }   // end of run ()
   
//**************************
//    FUNCTIONS PART
//**************************
    
    
//...............................................................
// Read what is in a FLAG file and Converts it into an Interger
//...............................................................
public int ReadFlag (String FileName) {

    int ReturnValue=0;

  // OPEN the given File 
  //.........................................................

              FileInputStream ReadFile = null;

                try {
                   ReadFile = new FileInputStream (FileName);
                }

                catch (Exception e) {
	               System.out.println (e);
	               //System.exit (1);
                 }

    // READ the file
    //..................................................................

             DataInputStream ds = new DataInputStream (ReadFile);
             
              try {
                      String s = ds.readLine (); // Read Data from the given File
   	          try {
                      ReturnValue = Integer.parseInt(s);
                      }
              catch (NumberFormatException e) {
                          System.out.println (e);
               	          //System.exit (1);
                      }
                  }
              catch (IOException e) {
                          System.out.println (e);
		          //System.exit (1);
                  }

      //Close File

      try {
            ReadFile.close ();
      }
      catch (IOException e) {
            System.out.println (e);
      }

                System.out.println ("Flag Value = "+ ReturnValue);

      return ReturnValue;
   } // end of FUNCTION
   
   
}   // END of OutServer class


//================================================================
// * class creates a server socket for RECEIVING data from
// * the client
//=================================================================
class InServer implements Runnable {

   ServerSocket server = null;    //Instance of ServerSocket
   Socket socket = null;          //The actual socket used for RECEIVING data

   int thePort;                   //Port number
   Thread thread;                 //A seperate thread is used to wait for a socket accept

   String QlockFile = "/var/www/ebusiness/b-f19-06/html/files/ClientSocket/f-Qs.dat";  // Flag-File for writting QUESTION (from the CLIENT)

   String fnameSI = "INCOMING.dat";      // Name of the File (by default) containning I_data at Server

   DataInputStream stream = null; //A DataInputStream is used for RECEIVING data

   /*
    * constructor starts the thread
    * @param port - the port to listen to
    */ 
     
   public InServer (int port) {

      thePort = port;
      thread = new Thread (this);
      thread.start ();
   }

   /*
    * the thread that waits for socket
    * connections and RECEIVES data from the client
    */
   public void run () {

      // Create a ServerSocket
      //.......................................   

      try {
         server = new ServerSocket (thePort);
         System.out.println ("OPEN a socket for RECEIVING data from the CLIENT at port " + thePort);
      }
      catch (Exception e) {
         System.out.println (e);
         System.exit (1);
      }
     
      while (true) {
         try {
            socket = server.accept ();
            System.out.println ("Connected to port : " + thePort);
         }
         catch (Exception e) {
            System.out.println (e);
            System.exit (1);
         }
         
         
     try {
            Process p = Runtime.getRuntime().exec("python /var/www/ebusiness/b-f19-06/html/cgi-bin/newSerb.cgi"); //serb.cgi
         }
      catch (Exception e) {
            System.out.println(e);
         }  
    

         // Accept file name "name" from the Client
         // ( Client tells WHICH FILE it wants to WRITE )
         //...............................................................
         String name = null;
         try {
            // Prepare a stream for RECEIVING
            stream = new DataInputStream (socket.getInputStream ());

            //Get File name from the CLIENT
            name = stream.readLine ();
            if (name == null) name = fnameSI;
         }
         catch (Exception e) {
            System.out.println (e);
            break;
         }
            

         // Open the given FILE
         //........................................................
         FileOutputStream wf = null;
         try {
            wf = new FileOutputStream (name);
         }
         catch (Exception e) {
            System.out.println (e);
            System.exit (1);
         }


         // Read Data from the "stream" and WRITE it to the given File
         //...........................................................

         PrintStream ds = new PrintStream (wf); // Why do we need this ???
         while (true) {
            try {
               String s = stream.readLine ();
               if (s == null) break;
               ds.println (s); // Why not just fs.println (s); ???
            }
            catch (IOException e) {
               System.out.println (e);
               break;
            }
         }

   // WRITE "1" to the LOCK(FLAG) of the ANSWER 
   //........................................................
   WriteFlag(QlockFile,"1");

         System.out.println ("   RECEIVING and writing data to file " + name +", done.");

         try {
            wf.close ();
            socket.close ();
            System.out.println ("Connection closed at port : " + thePort + " and Continue to LISTEN ...");
         }
         catch (IOException e) {
            System.out.println (e);
         }
      }
      
   }
   
//**************************
//    FUNCTIONS PART
//**************************

//=========================================================================
//      WRITE a Value to the FLAG File 
//=========================================================================

   public void WriteFlag (String FlagFileName, String FlagValue) {
   
         // Open the a FILE at Client site to WRITE
         //........................................................

         FileOutputStream wf = null;

         try {
            wf = new FileOutputStream (FlagFileName);
         }

         catch (Exception e) {
            System.out.println (e);
            System.exit (1);
         }

         // WRITE Value to the FILE 
         //........................................................

         PrintStream ds = new PrintStream (wf); // Create Output Sream to WRITE
         ds.println (FlagValue); 
      
      //Close File
      try {
         wf.close ();
      }
      catch (IOException e) {
         System.out.println (e);
      }

   }  // end of WriteFlag

   
} // END of CLASS InServer

