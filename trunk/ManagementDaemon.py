from UnixDaemon import UnixDaemon
from daemonCode import *
from ManagementXMLRPC import *
import time
class ManagementDaemon(UnixDaemon):
    def __init__(self,service, pidfile, name):
        UnixDaemon.__init__(self,pidfile=pidfile, name=name)
        self.service= service
        self.logger.info("Management Daemon Created")
    def run(self):
        self.logger.info("Starting Management Daemon")
        startManagementInterface(self.service,self.logger)
        self.logger.info("Management Daemon Started")