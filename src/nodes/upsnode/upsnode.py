import os
import time
from core.i2cnode import I2CNode
from threading import Thread, Event

class UPSNode(I2CNode):
    def __init__(self):
        super().__init__(name=__name__, address=self.UPSHAT)
    
    def start(self): 
        super().start()
        
        if self.running:
            self.battery_threshold = int(os.getenv("BATTERY_THRESHOLD"))
            self.run_every(30, self.get_battery_status)
    
    def get_battery_status(self):
        lo = self.read_data_byte(self.UPSHAT_BATTERY_PERCENTAGE_LO)      
        hi = self.read_data_byte(self.UPSHAT_BATTERY_PERCENTAGE_HI)      
        percent = 256*hi+lo
        self.node_event_channel.publish("ups-battery-percent", percent = percent)

        if percent < self.battery_threshold:
            self.node_event_channel.publish("under-voltage-detected")

