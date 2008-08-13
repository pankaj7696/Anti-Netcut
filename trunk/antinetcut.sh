#!/bin/bash
# ******** Ahmed Soliman Anti-NetCut v 0.2 *********#
# For More Information Visit www.AhmedSoliman.com 
# Part of HackRoot CAT-Hackers Distro. 

#checking dependencies
if rpm -q iproute > /dev/null
then
	echo "Dependencies OK"
else
	echo "Please install iproute suite, yum install iproute"
	exit 2
fi

#Configuration Section
INT=`ip route list | grep "default" | cut -d" " -f5` #Your Network Interface, Autodetected
if [ "$INT" = "" ] 
then
	echo "Couldn't autodetect your ethernet card that's connected to the internet."
	exit 1;
fi
echo "Intelligent Anti Netcut Utility"
echo "Written By ***Ahmed Soliman (www.ahmedsoliman.com) <h4ck3r@cat-hackers.com>****"

# Get Default Gateway IP Address
GW=`ip route list | grep "default" | cut -d" " -f3`
if [ "$GW" = "" ]
then
	echo "We Couldn't get your gateway IP Address, please check your internet settings"
	exit 1
fi
# Get Gateway Real MAC Address, strange method by efficient.
MAC=`arping -I $INT -f $GW | grep "Unicast" | cut -d" " -f5 | cut -d"[" -f2 | cut -d"]" -f1`
# Check whether our arp table stating the real mac or not.
ARP_MAC=`ip neigh list | grep "$GW" | cut -d" " -f5 | tr 'a-z' 'A-Z'`

if [ "$ARP_MAC" = "" ]
then
	#We Don't have The Gateway in the arp table, add it statically then.
	echo "The Gateway wasn't found in the arp table. This is strange but we will add it to the arp table statically, this hopefully should eliminate any further arp attacks"
	arp -i "$INT" -s "$GW" "$MAC"
	echo "Thank you."
	exit 0
fi

if [ "$ARP_MAC" != "$MAC" ]
then
	#We have a poisoner here, flush arp table and add static gateway entry.
	echo "Poisoning was detected, arp flusher will run and gateway address will be statically added, this hopefully should eliminate any further arp attacks."
	IP_LIST=`arp -n | grep "^[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+"| cut -d" " -f 1`
		echo "$IP_LIST" | while read ip ; do
	        	    /sbin/arp -d $ip
		done
	arp -i "$INT" -s "$GW" "$MAC"
	echo "Thank you."
	exit 0
else
	echo "Everything seems to be working fine, nothing was done."
	exit 1
fi
