from UnixDaemon import UnixDaemon
from daemonCode import *
from ManagementXMLRPC import *
from ManagementDaemon import *
import sys,time

class AntiNetCut(UnixDaemon):
    def run(self):
            self.logger.info("Starting Service")
            try:
                self.shouldRun = False
                firstRun = True
                while self.shouldRun== False:
                    if firstRun==True:
                        self.shouldRun = True
                    while self.shouldRun== True:
                        self.logger.error("HEY")
                        time.sleep(3)
                    firstRun= False
                    time.sleep(2)
            except:
                self.logger.error("Unexpected Error, Terminating %s" % str(sys.exc_info()))
    def startService(self):
        self.shouldRun = True
        return True
    def stopService(self):
        self.shouldRun = False
        return True
            #runAntiNetCut(self.logger)
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