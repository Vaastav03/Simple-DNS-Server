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
import sys
import socket

nrip='127.0.0.1'
startportnum=int(sys.argv[1])
fn=str(sys.argv[2])
f=open(fn,"r")
#file for the RDS output
rdsfd=open("RDS.output","w")
#database in the root dns that contains the IP adresses of the TDSs
rdns={}
#dictionary that contains the portnumbers of the TDS
tlds={}
#parse the input file
line=f.readline().strip()
while True:
    if line=="BEGIN_DATA":
        for i in range(2):
            line=f.readline().strip()
        for i in range(2):
            line=f.readline().strip()
            line=line.split()
            rdns[line[0]]=line[1]
            tlds[line[0]]=startportnum+55+i
        break
#rds socket
rdserver=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#bind it to the startportnum+54 port
rdserver.bind((nrip,startportnum+54))
#rds up and listening
while True:
    #recieve the message from the name resolver
    msgfromnr,addr=rdserver.recvfrom(1024)
    msg=msgfromnr.decode()
    rdsfd.write("Query from NR: "+msg+"\n")
    #exit message processing
    if msg=="bye":
        #send the bye message to tlds 
        rdserver.sendto(msgfromnr,(nrip,startportnum+55))
        rdserver.sendto(msgfromnr,(nrip,startportnum+56))
        rdsfd.write("Response to TDS_1 and TDS_2: "+msg+"\n")
        rdsfd.close()
        sys.exit(0)
    else:
        sname=msg.split(".")
        n=len(sname)
        s='TDS_'+sname[n-1]
        #if the rdns has the tds then we send the IP of the tds and its portnum
        if s in rdns:
            TDSport=tlds[s]
            msgtonr=rdns[s]+" "+str(TDSport)
            #send the message to the name resolver
            rdsfd.write("Response to NR: "+msgtonr+"\n")
            rdserver.sendto(msgtonr.encode(),addr)
        #else send the record not fount message to the name resolver
        else:
            msgtonr="No DNS Record Found"
            rdsfd.write("Response to NR: "+msgtonr+"\n")
            rdserver.sendto(msgtonr.encode(),addr)