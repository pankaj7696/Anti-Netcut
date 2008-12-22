import SimpleXMLRPCServer
import sys,os
class ManagementInterface:
    def __init__(self,daemon):
        self.daemon= daemon
    def stop(self):
        self.daemon.stopService()
        return True
    def start(self):
        #we need to fork to ensure no zombies are created
        self.daemon.startService()
        return True
    def restart(self):
        self.daemon.restart()
        return True
    def status(self):
        return self.daemon.status()
    
def startManagementInterface(daemon,logger):
    logger.info("Starting XMLRPC Server")
    try:
        server = SimpleXMLRPCServer.SimpleXMLRPCServer(('localhost',46201))
        server.register_instance(ManagementInterface(daemon))
        server.serve_forever()
        logger.info("Starting XMLRPC Server")
    except:
        logger.error("Error starting XMLRPC Server")
    #TODO: Implement this...
    #def checkIfUnderAttack(self):
    #    pass