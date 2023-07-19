# NAME:Pitchika Vaastav
# Roll Number:CS20B060
# Course: CS3205 Jan. 2023 semester
# Lab number: 2
# Date of submission: March 4th , 2023
# I confirm that the source file is entirely written by me without
# resorting to any dishonest means.
# Website(s) that I used for basic socket programming code are:
# URL(s): https://www.geeksforgeeks.org/file-handling-python/
#https://www.geeksforgeeks.org/python-exit-commands-quit-exit-sys-exit-and-os-_exit/
#https://www.geeksforgeeks.org/creating-child-process-using-fork-python/
import os
import socket
import sys
import time

#command line arguments
startportnum=int(sys.argv[1])
fn=str(sys.argv[2])
nrip='127.0.0.1'

#forking 10 servers as child processes
for i in range(10):
    pid=os.fork()
    if pid==0:
        if i==0:
            #RDS
            os.system("python rds.py "+str(startportnum)+" "+fn)
            sys.exit(0)
        elif i==1:
            #TDS_1
            os.system("python tds1.py "+str(startportnum)+" "+fn)
            sys.exit(0)
        elif i==2:
            #TDS_2
            os.system("python tds2.py "+str(startportnum)+" "+fn)
            sys.exit(0)
        elif i==3:
            #ads1
            os.system("python ads1.py "+str(startportnum)+" "+fn)
            sys.exit(0)
        elif i==4:
            #ads2
            os.system("python ads2.py "+str(startportnum)+" "+fn)
            sys.exit(0)
        elif i==5:
            #ads3
            os.system("python ads3.py "+str(startportnum)+" "+fn)
            sys.exit(0)
        elif i==6:
            #ads4
            os.system("python ads4.py "+str(startportnum)+" "+fn)
            sys.exit(0)
        elif i==7:
            #ads5
            os.system("python ads5.py "+str(startportnum)+" "+fn)
            sys.exit(0)
        elif i==8:
            #ads6
            os.system("python ads6.py "+str(startportnum)+" "+fn)
            sys.exit(0)
        elif i==9:
            #nr
            os.system("python NR.py "+str(startportnum)+" "+fn)
            sys.exit(0)

#wait till all the servers are up and running
time.sleep(5)
#client UDP socket created
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
#starts accepting the user inputs
while True:
    msgFromClient=input("Enter Server Name: ")
    #user gives exit message
    if msgFromClient=="bye":
        #send the exit message to name resolver
        bytesToSend=str.encode(msgFromClient)
        UDPClientSocket.sendto(bytesToSend, (nrip,startportnum+53))
        print("All Server Processes are killed. Exiting.")
        sys.exit(0)
    else:
        #send query to name resolver
        bytesToSend=str.encode(msgFromClient)
        UDPClientSocket.sendto(bytesToSend, (nrip,startportnum+53))
        #recieve response on the port
        smsg,saddr = UDPClientSocket.recvfrom(1024)
        msg=smsg.decode()
        #if the message is "No DNS Record Found" then print that
        if msg=="No DNS Record Found":
            print("No DNS Record Found")
        #if the message is "Invalid Server Name" then print that
        elif msg=="Invalid Server Name":
            print("Invalid Server Name")
        #else print the IP recieved
        else:
            print("DNS Mapping: "+msg)
