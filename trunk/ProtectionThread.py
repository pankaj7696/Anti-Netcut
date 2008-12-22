import threading
from scapy.all import *
import time
class ProtectionThread(threading.Thread):
    """The Protection Thread"""
    
    def __init__(self,p1,p2,logger):
        self.packet1 = p1
        self.packet2 = p2
        self.logger = logger
        self.shouldRun = True
    
    def run(self):
        self.logger.info("Protection Thread Started..")
        while self.shouldRun:
            sendp(self.packet1, verbose=0)
            sendp(self.packet2,verbose=0)
            time.sleep(0.7)