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

#Name Resolver output file
nrfd=open("NR.output","w")

#Name resolver server socket setup
nrserver=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#Bind the NR server on the mentioned port
nrserver.bind((nrip,startportnum+53))

#NR server up and listening
while True:
    #recieve the message from the client
    msgfromclient,addr=nrserver.recvfrom(1024)
    msg=msgfromclient.decode()
    #exit message processing
    if msg=="bye":
        #send the exit message to root dns server
        nrserver.sendto(msgfromclient,(nrip,startportnum+54))
        nrfd.write("Query from Client: "+msg+"\n")
        nrfd.write("Response to RDS: "+msg+"\n")
        nrfd.close()
        sys.exit(0)
    #incorrect domain format
    elif len(msg.split('.'))<3:
        nrfd.write("Query from Client: "+msg+"\n")
        #send no record found message to the client
        msg="Invalid server name"
        nrfd.write("Response to Client: "+msg+"\n")
        nrserver.sendto(msg.encode(),addr)
        continue
    nrfd.write("Query from Client: "+msg+"\n")
    #send the domain to root dns
    nrserver.sendto(msgfromclient,(nrip,startportnum+54))
    nrfd.write("Query to RDS: "+msg+"\n")
    #recieve the message from root dns
    msgfromrds,raddr=nrserver.recvfrom(1024)
    rmsg=msgfromrds.decode()
    nrfd.write("Response from RDS: "+rmsg+"\n")
    #if we dont have the particular Top level domain in the RDS then 
    #we recieve No Record Found, so we report the same thing to client
    if rmsg=="No DNS Record Found":
        nrfd.write("Response to Client: "+rmsg+"\n")
        nrserver.sendto(msgfromrds,addr)
    #else we recieve the IP of the TDS
    else:
        #the message contains the IP of the TDS and the port number of the TDS
        TDSdata=rmsg.split(" ")
        TDSIP=TDSdata[0]
        TDSport=int(TDSdata[1])
        #send the domain to the designated TDS
        nrserver.sendto(msgfromclient,(TDSIP,TDSport))
        nrfd.write("Query to TDS: "+msg+"\n")
        #recieve the message from TDS
        msgfromtds,tdsaddr=nrserver.recvfrom(1024)
        tmsg=msgfromtds.decode()
        #if the particular authoritative domain not present in the TDS
        #then we recieve the No DNS Record Found message
        if tmsg=="No DNS Record Found":
            nrfd.write("Response from tds: "+tmsg+"\n")
            #send the message to the client
            nrserver.sendto(msgfromtds,addr)
            nrfd.write("Response to Client: "+tmsg+"\n")
        #else we recieve the IP and portnumber of the necessary ads
        else:
            nrfd.write("Response from tds: "+tmsg+"\n")
            ADSdata=tmsg.split(" ")
            ADSIP=ADSdata[0]
            ADSPORT=int(ADSdata[1])
            #send the domain name to the designated port
            nrserver.sendto(msgfromclient,(ADSIP,ADSPORT))
            nrfd.write("Query to ADS: "+msg+"\n")
            #recieve the message from ads
            msgfromads,adsaddr=nrserver.recvfrom(1024)
            amsg=msgfromads.decode()
            nrfd.write("Response from ADS: "+amsg+"\n")
            #send it to the client
            nrserver.sendto(msgfromads,addr)
            nrfd.write("Response to Client: "+amsg+"\n")