#! /usr/bin/env python


import sys
from scapy.all import *

def runAntiNetCut(logger):
    #YOU MUST CHANGE THIS TO MATCH YOUR DEVICE
    device="eth0"
    gw="" #Leave this if you want the automatic detection, enter your gateway if you want to turn the automatic detection off
    
    #DO NOT MODIFY UNDER THIS LINE
    logger.info("""
    Welcome To AntiNetCut Version 2.1
    Development done by AhmedSoliman.com <me@ahmedsoliman.com>
    Released December 2008""")
    
    if os.getuid():

       logger.error("Fatal Error: This must run as 'root'")
       sys.exit(2)
    if len(gw) > 0:
       gwIP=gw
    else:
       #get the IP address of the gateway
       pipe1 =os.popen("./getdefaultgw.sh",'r')
       gwIP=pipe1.readline()
       pipe1.close()
    #get the mac address of the gateway
    mac=getmacbyip(gwIP)
    if mac == None:
       logger.error("Fatal Error: We couldn't get the gateway MAC address, sorry")
       exit(3)
    logger.info( 'MAC Address Detected for the gateway %s %s' % (gwIP,mac))
    logger.info('Deleting Current gateway mac address from the arp table')
    if os.system("arp -d " +  gwIP):
       logger.error("Fatal Error: Couldn't delete the gateway from your arp table")
       exit(2)
    logger.info( 'Adding static entry...')
    if os.system("arp -s " + gwIP + " " + mac):
       logger.error("Couldn't add the static entry")
    
    #get my MAC address
    pipe2=os.popen("ip addr show dev " + device + "|awk '/ether/{ print $2 }'",'r')
    myMAC=pipe2.readline()
    myMAC=myMAC.strip("\n")
    pipe2.close()
    if not len(myMAC) > 0:
       logger.error("Fatal Error: Cannot Detect my MAC address")
       exit(3)
    #get my IP address
    pipe3=os.popen("ip addr show dev " +device+" |awk '/inet /{ print $2 }'",'r')
    myIP=pipe3.readline()
    myIP=myIP[:myIP.find("/")]
    pipe3.close()
    if not len(myIP) >0:
       logger.error("Fatal Error: Cannot Detect my IP address")
       exit(4)
    logger.info("Our IP Address is " + myIP)
    logger.info( "Out MAC Address is " + myMAC)
    logger.info( "Running Protection Thread")
    
    p1=Ether(dst="ff:ff:ff:ff:ff:ff",src=myMAC)/ARP(pdst="255.255.255.255",psrc=myIP,op=1,hwsrc=myMAC,hwdst="00:00:00:00:00:00")
    p2=Ether(dst="ff:ff:ff:ff:ff:ff",src=myMAC)/ARP(pdst=gwIP,psrc=myIP,op=2,hwsrc=myMAC,hwdst=mac)
    #p1=ARP()
    #p1.op=1
    #p1.hwsrc=myMAC
    #p1.hwdst="00:00:00:00:00:00"
    #p1.psrc=myIP
    #p1.pdst="255.255.255.255"
    
    #p2=ARP()
    #p2.op=2
    
    while 1:
       sendp(p1,verbose=0)
       sendp(p2,verbose=0)
       time.sleep(.7)
    #print 'Hello World'
