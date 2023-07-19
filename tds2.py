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

nrip='127.0.0.1'
startportnum=int(sys.argv[1])
fn=str(sys.argv[2])
f=open(fn,"r")
#output for the TDS2
tdsefd=open("TDS_2.output","w")
#database for the IP addresses of the ads under the tld
tld2={}
#map for the ads and domain name
adsmap={}
#parse the input
line=f.readline().strip()
while line!="END_DATA":
    if line=="BEGIN_DATA":
        for i in range(7):
            line=f.readline().strip()
        for i in range(3):
            line=f.readline().strip()
            d=line.split()
            tld2[d[0]]=d[1]
    if line=="List_of_ADS1":
        for i in range(17):
            line=f.readline().strip()
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
#tds setup
tdserver=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#tds bind to startportnum+56
tdserver.bind((nrip,startportnum+56))
#tds up and listening
while True:
    #recieve message from the name resolver
    msgfromnr,addr=tdserver.recvfrom(1024)
    msg=msgfromnr.decode()
    #exit message processing
    if msg=="bye":
        #send the bye message to ads under the tld2
        tdsefd.write("Query from RDS "+msg+"\n")
        tdserver.sendto(msgfromnr,(nrip,startportnum+60))
        tdserver.sendto(msgfromnr,(nrip,startportnum+61))
        tdserver.sendto(msgfromnr,(nrip,startportnum+62))
        tdsefd.write("Response to ADS: "+msg+"\n")
        tdsefd.close()
        sys.exit(0)
    sname=msg.split(".")
    n=len(sname)
    aname=sname[n-2]+"."+sname[n-1]
    tdsefd.write("Query from NR: "+msg+"\n")
    #if the authoritative name in the adsmap then send its ip and portnumber to name resolver
    if aname in adsmap:
        msgtonr=""
        if adsmap[aname]=="ADS4":
            msgtonr=tld2[aname]+" "+str(startportnum+60)
        if adsmap[aname]=="ADS5":
            msgtonr=tld2[aname]+" "+str(startportnum+61)    
        if adsmap[aname]=="ADS6":
            msgtonr=tld2[aname]+" "+str(startportnum+62)
        tdsefd.write("Response to NR: "+msgtonr+"\n")   
        tdserver.sendto(msgtonr.encode(),addr)
    #else send the no record found message to the name resolver
    else:
        msgtonr="No DNS Record Found"
        tdsefd.write("Message to NR: "+msgtonr+"\n")
        tdserver.sendto(msgtonr.encode(),addr)