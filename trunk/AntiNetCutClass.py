from UnixDaemon import UnixDaemon
from daemonCode import *
from ManagementXMLRPC import *
from scapy.all import *
import sys,time

class AntiNetCut(UnixDaemon):
    def __init__(self,pidfile,name):
        UnixDaemon.__init__(self,pidfile=pidfile,name=name)
        self.protectionThread = None
        self.resume()
    def run(self):
            self.logger.info("Starting Service")
            self.management = startManagementInterface(self,self.logger)
            self._startAntiNetCut()
    def waitLoop(self):
        while not self.shouldRun:
            time.sleep(1)
            self.logger.info("Waiting Loop")
            
    def terminate(self):
        self.shouldRun = False
        self.shouldTerminate = True
        
    def resume(self):
        self.logger.info("Resume Called..")
        self.shouldTerminate = False
        self.shouldRun = True
        
    def pause(self):
        self.logger.info("Pause Called..")
        self.shouldTerminate = False
        self.shouldRun = False
        
    def _startAntiNetCut(self):
        gw="" #Leave this if you want the automatic detection, enter your gateway if you want to turn the automatic detection off
        
        #DO NOT MODIFY UNDER THIS LINE
        self.logger.info("""
        *** Welcome To AntiNetCut Version 0.25 ***
        *** Development done by AhmedSoliman.com <me@ahmedsoliman.com> ***
        """)
        
        if os.getuid():
           self.logger.error("Fatal Error: This must run as 'root'")
           sys.exit(2)
        if len(gw) > 0:
           gwIP=gw
        else:
            gwIP = None
            for i in read_routes():
                if i[0] == 0:
                    gwIP = i[2]
                    device = i[3]
        if not gwIP:
            self.logger.error("Fatal Error: There is no gateway detected, Please specify it in the configuration file.")
            sys.exit(5)
        mac=getmacbyip(gwIP)
        if mac == None:
           self.logger.error("Fatal Error: We couldn't get the gateway MAC address, sorry")
           exit(3)
        self.logger.info( 'MAC Address Detected for the gateway %s %s' % (gwIP,mac))
        self.logger.info('Deleting Current gateway mac address from the arp table')
        if os.system("arp -d " +  gwIP):
           self.logger.error("Error: Couldn't delete the gateway from your arp table")

        self.logger.info( 'Adding static entry...')
        if os.system("arp -s " + gwIP + " " + mac):
           self.logger.error("Couldn't add the static entry: %s" % sys.exc_info())
        #get my MAC address
        myMAC = get_if_hwaddr(device)
        pipe2.close()
        if not len(myMAC) > 0:
           self.logger.error("Fatal Error: Cannot Detect my MAC address: %s" % sys.exc_info())
           exit(3)
        #get my IP address
        myIP = get_if_addr(device)
        if not len(myIP) >0:
           self.logger.error("Fatal Error: Cannot Detect my IP address: %s" % sys.exc_info())
           exit(4)
        self.logger.debug("Our IP Address is " + myIP)
        self.logger.debug( "Our MAC Address is " + myMAC)
        p1=Ether(dst="ff:ff:ff:ff:ff:ff",src=myMAC)/ARP(pdst="255.255.255.255",psrc=myIP,op=1,hwsrc=myMAC,hwdst="00:00:00:00:00:00")
        p2=Ether(dst="ff:ff:ff:ff:ff:ff",src=myMAC)/ARP(pdst=gwIP,psrc=myIP,op=2,hwsrc=myMAC,hwdst=mac)
        
        self.logger.info("Protection Thread Started..")
        while not self.shouldTerminate:
            while self.shouldRun:
                self.logger.debug("Run Now")
                sendp(p1, verbose=0)
                sendp(p2,verbose=0)
                self.logger.debug("Sending Correction Packet")
                time.sleep(0.7)
            self.logger.debug("Waiting...")
            self.waitLoop()