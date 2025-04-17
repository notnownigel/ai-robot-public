import os
import time
from core.i2cnode import I2CNode

class BuzzerNode(I2CNode):
    def __init__(self):
        super().__init__(name=__name__, address=self.RASPBOT)
    
    def start(self): 
        super().start()
        
        if self.running:
            self.node_event_channel.subscribe("buzzer-node-sound", self.sound_buzzer)
            
            if int(os.getenv("BEEP_ON_STARTUP")) != 0:
                self.sound_buzzer(0.1)
    
    def sound_buzzer(self, duration):
        self.write_data_byte(I2CNode.RASPBOT_BUZZER, I2CNode.RASPBOT_BUZZER_ON)
        time.sleep(duration)
        self.write_data_byte(I2CNode.RASPBOT_BUZZER, I2CNode.RASPBOT_BUZZER_OFF)
