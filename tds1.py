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
#output file for TDS1
tdscfd=open("TDS_1.output","w")
#TLD database for the IP addresses of the ADSs
tld1={}
#dictionary for mapping the domains to the ADS
adsmap={}
#parsing the input file
line=f.readline().strip()
while(line!="END_DATA"):
    if line=="BEGIN_DATA":
        for i in range(4):
            line=f.readline().strip()
        for i in range(3):
                line=f.readline().strip()
                d=line.split()
                tld1[d[0]]=d[1]
        for i in range(3):
                line=f.readline().strip()
    if line=="List_of_ADS1":
        for i in range(5):
            line=f.readline().strip()
            d=line.split()
            d1=d[0].split(".")
            n=len(d1)
            a=d1[n-2]+"."+d1[n-1]
            adsmap[a]="ADS1"
    if line=="List_of_ADS2":
        for i in range(5):
            line=f.readline().strip()
            d=line.split()
            d1=d[0].split(".")
            n=len(d1)
            a=d1[n-2]+"."+d1[n-1]
            adsmap[a]="ADS2"
    if line=="List_of_ADS3":
        for i in range(5):
            line=f.readline().strip()
            d=line.split()
            d1=d[0].split(".")
            n=len(d1)
            a=d1[n-2]+"."+d1[n-1]
            adsmap[a]="ADS3"
    if line=="List_of_ADS4":
        for i in range(5):
            line=f.readline().strip()
            d=line.split()
            d1=d[0].split(".")
            n=len(d1)
            a=d1[n-2]+"."+d1[n-1]
            adsmap[a]="ADS4"
    if line=="List_of_ADS5":
        for i in range(5):
            line=f.readline().strip()
            d=line.split()
            d1=d[0].split(".")
            n=len(d1)
            a=d1[n-2]+"."+d1[n-1]
            adsmap[a]="ADS5"
    if line=="List_of_ADS6":
        for i in range(5):
            line=f.readline().strip()
            d=line.split()
            d1=d[0].split(".")
            n=len(d1)
            a=d1[n-2]+"."+d1[n-1]
            adsmap[a]="ADS6"
    line=f.readline().strip()

#TDS socket setup
tdserver=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#TDS bind to the startportnum+55
tdserver.bind((nrip,startportnum+55))
while True:
    #recieve the message from name resolver
    msgfromnr,addr=tdserver.recvfrom(1024)
    msg=msgfromnr.decode()
    #exit message processing
    if msg=="bye":
        #send the bye message to all the ads under the tds
        tdscfd.write("Query from RDS "+msg+"\n")
        tdserver.sendto(msgfromnr,(nrip,startportnum+57))
        tdserver.sendto(msgfromnr,(nrip,startportnum+58))
        tdserver.sendto(msgfromnr,(nrip,startportnum+59))
        tdscfd.write("Response to ADS: "+msg+"\n")
        tdscfd.close()
        sys.exit(0)
    sname=msg.split(".")
    n=len(sname)
    aname=sname[n-2]+"."+sname[n-1]
    tdscfd.write("Query from NR: "+msg+"\n")
    #if the authoritative domain name in the adsmap
    #then send the IP of the necessary ADS and it's portnumber
    if aname in adsmap:
        msgtonr=""
        if adsmap[aname]=="ADS1":
            msgtonr=tld1[aname]+" "+str(startportnum+57)
        if adsmap[aname]=="ADS2":
            msgtonr=tld1[aname]+" "+str(startportnum+58)    
        if adsmap[aname]=="ADS3":
            msgtonr=tld1[aname]+" "+str(startportnum+59)
        tdscfd.write("Response to NR: "+msgtonr+"\n")   
        tdserver.sendto(msgtonr.encode(),addr)
    #else send the record not found message to the name resolver
    else:
        msgtonr="No DNS Record Found"
        tdscfd.write("Message to NR: "+msgtonr+"\n")
        tdserver.sendto(msgtonr.encode(),addr)