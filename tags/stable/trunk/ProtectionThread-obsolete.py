import threading
from scapy.all import *
import time
class ProtectionThread(threading.Thread):
    """The Protection Thread"""
    
    def __init__(self,p1,p2,logger):
        self.packet1 = p1
        self.packet2 = p2
        self.logger = logger
        self.resume()
        
    def terminate(self):
        self.shouldRun = False
        self.shouldTerminate = True
        
    def resume(self):
        self.shouldTerminate = False
        self.shouldRun = True
        
    def pause(self):
        self.shouldTerminate = False
        self.shouldRun = False
        
    def waitLoop(self):
        while not self.shouldRun:
            time.sleep(1)

    def run(self):
        self.logger.info("Protection Thread Started..")
        while not self.shouldTerminate:
            while self.shouldRun:
                sendp(self.packet1, verbose=0)
                sendp(self.packet2,verbose=0)
                time.sleep(0.7)
            waitLoop()