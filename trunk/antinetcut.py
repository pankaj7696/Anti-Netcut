from UnixDaemon import UnixDaemon
from daemonCode import *
from ManagementXMLRPC import *
from ManagementDaemon import *
from ProtectionThread import *
from scapy.all import *
import sys,time

class AntiNetCut(UnixDaemon):
    def __init__(self,pidfile,name):
        UnixDaemon.__init__(self,pidfile=pidfile,name=name)
        self.protectionThread = None
        self.firstRun = True
        self.shouldRun = False
    def run(self):
            self.logger.info("Starting Service")
            try:

                while self.shouldRun== False:
                    if self.firstRun==True:
                        self.shouldRun = True
                    self._startAntiNetCut()
                    while self.shouldRun== True:
                        time.sleep(2)
                    self.firstRun= False
                    time.sleep(2)
            except:
                self.logger.error("Unexpected Error, Terminating %s" % str(sys.exc_info()))
    def startService(self):
        self.logger.info("Stopping Protection Thread from XMLRPC Command..")
        self.shouldRun = True
        return True
    def stopService(self):
        self.logger.info("Stopping Protection Thread from XMLRPC Command..")
        self.shouldRun = False
        self.protectionThread.shouldRun = False
        return True
    def _startAntiNetCut(self):
        #YOU MUST CHANGE THIS TO MATCH YOUR DEVICE
        device="eth1"
        gw="" #Leave this if you want the automatic detection, enter your gateway if you want to turn the automatic detection off
        
        #DO NOT MODIFY UNDER THIS LINE
        self.logger.info("""
        Welcome To AntiNetCut Version 2.1
        Development done by AhmedSoliman.com <me@ahmedsoliman.com>
        Released December 2008""")
        
        if os.getuid():
    
           self.logger.error("Fatal Error: This must run as 'root'")
           sys.exit(2)
        if len(gw) > 0:
           gwIP=gw
        else:
           #get the IP address of the gateway
           self.logger.info("Running %s" % (sys.path[0] + "/getdefaultgw.sh")) 
           pipe1 =os.popen(sys.path[0] + "/getdefaultgw.sh",'r')
           gwIP=pipe1.readline()
           pipe1.close()
        #get the mac address of the gateway
        self.logger.info("The Gateway is %s" % gwIP)
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
           self.logger.error("Fatal Error: Couldn't delete the gateway from your arp table")
           exit(2)
        self.logger.info( 'Adding static entry...')
        if os.system("arp -s " + gwIP + " " + mac):
           self.logger.error("Couldn't add the static entry")
        
        #get my MAC address
        pipe2=os.popen("ip addr show dev " + device + "|awk '/ether/{ print $2 }'",'r')
        myMAC=pipe2.readline()
        myMAC=myMAC.strip("\n")
        pipe2.close()
        if not len(myMAC) > 0:
           self.logger.error("Fatal Error: Cannot Detect my MAC address")
           exit(3)
        #get my IP address
        pipe3=os.popen("ip addr show dev " +device+" |awk '/inet /{ print $2 }'",'r')
        myIP=pipe3.readline()
        myIP=myIP[:myIP.find("/")]
        pipe3.close()
        if not len(myIP) >0:
           self.logger.error("Fatal Error: Cannot Detect my IP address")
           exit(4)
        self.logger.info("Our IP Address is " + myIP)
        self.logger.info( "Out MAC Address is " + myMAC)
        self.logger.info( "Running Protection Thread")
        
        p1=Ether(dst="ff:ff:ff:ff:ff:ff",src=myMAC)/ARP(pdst="255.255.255.255",psrc=myIP,op=1,hwsrc=myMAC,hwdst="00:00:00:00:00:00")
        p2=Ether(dst="ff:ff:ff:ff:ff:ff",src=myMAC)/ARP(pdst=gwIP,psrc=myIP,op=2,hwsrc=myMAC,hwdst=mac)
        self.protectionThread = ProtectionThread(p1,p2,self.logger)
        self.protectionThread.start()
def main(): 
    service = AntiNetCut(pidfile = '/var/run/antinetcut.pid',name='antinetcut')
    management = ManagementDaemon(service= service, pidfile = '/var/run/antinetcut-XMLRPC.pid',name='antinetcut-XMLRPC')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            management.start()
            service.start()
            sys.exit(0)
        elif 'stop' == sys.argv[1]:
            service.stop()
            management.stop()
        elif 'status' == sys.argv[1]:
            ret = service.status()
            if ret:
                print "Antinetcut daemon is running..."
            else:
                print "Antinetcut daemon is NOT running..."

            ret2 = management.status()
            if ret2:
                print "Antinetcut management daemon is running..."
            else:
                print "Antinetcut management daemon is NOT running..."
            
        elif 'restart' == sys.argv[1]:
            service.restart()
        else:
            print "Invalid argument"
            printUsage()
        sys.exit(0)
    else:
        printUsage()
def printUsage():
    print "Usage: %s start|stop|status|restart" % sys.argv[0]
    sys.exit(2)

if __name__ == "__main__":
    main()