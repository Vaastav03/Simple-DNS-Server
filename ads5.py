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

#file to write the output of the ads
afd=open("ads5.output","w")

#ads database stored in a dictionary
ads={}

#parsing the input file and populating the ads1 database
line=f.readline().strip()
while(line!="List_of_ADS5"):
    line=f.readline().strip()
for i in range(5):
    line=f.readline().strip()
    d=line.split()
    ads[d[0]]=d[1]

#creating a UDP socket for ads5
adserver=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#binding the socket to the port number startportnum+61 as given in question
adserver.bind((nrip,startportnum+61))
#server starts listening for requests
while True:
    #receive the message from the name resolver
    msgfromnr,addr=adserver.recvfrom(1024)
    msg=msgfromnr.decode()
    #exit message processing
    if msg=="bye":
        afd.write("Query from TDS: "+msg+"\n")
        afd.write("Response : "+msg+"\n")
        afd.close()
        sys.exit(0)
        
    afd.write("Query from NR: "+msg+"\n")

    #if the domain(message) is in ads5
    if msg in ads:
        #send the ip of the domain to the name resolver
        msgtonr=ads[msg]
        afd.write("Response to NR: "+msgtonr+"\n")
        adserver.sendto(msgtonr.encode(),addr)
    #if the domain is not present in the database
    else:
        #send the prompt message
        msgtonr="No DNS Record Found"
        afd.write("Message to NR: "+msgtonr+"\n")
        adserver.sendto(msgtonr.encode(),addr)