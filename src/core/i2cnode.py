from .node import Node 
from smbus2 import SMBus 

# Base class for I2C Node
class I2CNode(Node):
    
    # RASPBOT I2C Specifics
    RASPBOT = 0x2B
    
    RASPBOT_KEY = 0x0D

    RASPBOT_BUZZER = 0x06
    RASPBOT_BUZZER_ON = 0x01
    RASPBOT_BUZZER_OFF = 0x00
    
    RASPBOT_SERVO = 0x02

    RASPBOT_MOTOR = 0x01

    # Waveshare UPS HAT I2C Specifics
    UPSHAT = 0x2D
    UPSHAT_BATTERY_PERCENTAGE_LO = 0x24
    UPSHAT_BATTERY_PERCENTAGE_HI = 0x25

    def get_i2c_device(self, address, i2c_bus=1):
        self.addr = address
        return SMBus(i2c_bus)

    def failure(self, register, readwrite):
        self.warning(f"Failed to {readwrite} I2C register {hex(register)}")
        self.stop()
        
    def __init__(self, name, address):
        super().__init__(name=name)
        self.device = self.get_i2c_device(address)

    def write_data_byte(self, reg, data):
        try:
            self.device.write_byte_data(self.addr, reg, data)
        except:
            self.failure(reg, "write to")

    def write_reg(self, reg):
        try:
            self.device.write_byte(self.addr, reg)
        except:
            self.failure(reg, "write to")

    def write_array(self, reg, data):
        try:
            self.device.write_i2c_block_data(self.addr, reg, data)
        except:
            self.failure(reg, "write to")

    def read_data_byte(self, reg):
        try:
            buf = self.device.read_byte_data(self.addr, reg)
            return buf
        except:
            self.failure(reg, "read from")

    def read_data_array(self, reg, len):
        try:
            buf = self.device.read_i2c_block_data(self.addr, reg, len)
            return buf
        except:
            self.failure(reg, "read from")
            self.stop()

    def start(self):
        super().start()
        # early discovery
        _ = self.read_data_byte(I2CNode.RASPBOT_KEY)

    def stop(self):
        super().stop()