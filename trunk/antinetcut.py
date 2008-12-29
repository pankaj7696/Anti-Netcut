from UnixDaemon import UnixDaemon
from ManagementXMLRPC import *
from AntiNetCutClass import *
from scapy.all import *
import sys,time,os

def main():
    #basic checking
    if os.getuid():
        print "Operation Not Permitted. User must be root."
        sys.exit(1)
    service = AntiNetCut(pidfile = '/var/run/antinetcut.pid',name='antinetcut')    
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            service.start()
            sys.exit(0)
            
        elif 'stop' == sys.argv[1]:
            service.stop()
            
        elif 'status' == sys.argv[1]:
            ret = service.status()
            if ret:
                print "Antinetcut daemon is running..."
            else:
                print "Antinetcut daemon is NOT running..."
                            
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