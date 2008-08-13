#! /usr/bin/env python


import sys
from scapy.all import *
#YOU MUST CHANGE THIS TO MATCH YOUR DEVICE

device="eth0"
gw="" #Leave this if you want the automatic detection, enter your gateway if you want to turn the automatic detection off

#DO NOT MODIFY UNDER THIS LINE
print """Welcome To AntiNetCut Version 2
Development done by AhmedSoliman.com <me@ahmedsoliman.com>
Released August 2008"""

if os.getuid():
   print ''
   print "This script must be run as 'root'"
   exit(2)
if len(gw) > 0:
   myIP=gw
else:
   #get the IP address of the gateway
   pipe1 =os.popen("./getdefaultgw.sh",'r')
   gwIP=pipe1.readline()
   pipe1.close()
#get the mac address of the gateway
mac=getmacbyip(gwIP)
if mac == None:
   print "We couldn't get the gateway MAC address, sorry"
   exit(3)
print 'MAC Address Detected for the gateway %s %s' % (gwIP,mac)
print 'Deleting Current gateway mac address from the arp table'
if os.system("arp -d " +  gwIP):
   print "Couldn't delete the gateway from your arp table"
   exit(2)
print 'Adding static entry...'
if os.system("arp -s " + gwIP + " " + mac):
   print "Couldn't add the static entry"

#get my MAC address
pipe2=os.popen("ip addr show dev " + device + "|awk '/ether/{ print $2 }'",'r')
myMAC=pipe2.readline()
myMAC=myMAC.strip("\n")
pipe2.close()
if not len(myMAC) > 0:
   print "Cannot Detect my MAC address"
   exit(3)
#get my IP address
pipe3=os.popen("ip addr show dev " +device+" |awk '/inet /{ print $2 }'",'r')
myIP=pipe3.readline()
myIP=myIP[:myIP.find("/")]
pipe3.close()
if not len(myIP) >0:
   print "Cannot Detect my IP address"
   exit(4)
print "Our IP Address is " + myIP
print "Out MAC Address is " + myMAC
print ''
print "Running Protection Thread"

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
