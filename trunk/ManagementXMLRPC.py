import SimpleXMLRPCServer
import thread
import sys,os

class ManagementInterface:
    def __init__(self,daemon):
        self.daemon= daemon
        
    def stop(self):
        self.daemon.pause()
        return True
    
    def start(self):
        self.daemon.resume()
        return True
    
    def status(self):
        return self.daemon.protectionStatus()
    
def startManagementInterface(daemon,logger):
    logger.info("Starting XMLRPC Server")
    try:
        server = SimpleXMLRPCServer.SimpleXMLRPCServer(('localhost',46201))
        server.register_instance(ManagementInterface(daemon))
        logger.info("Starting XMLRPC Server on localhost:46201")
        thread.start_new_thread(server.serve_forever,tuple())
    except:
        logger.error("Error starting XMLRPC Server: %s" % sys.exc_info())
    #TODO: Implement this...
    #def checkIfUnderAttack(self):
    #    pass