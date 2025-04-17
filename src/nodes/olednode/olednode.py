import board
import busio
import adafruit_ssd1306
from core.node import Node
from PIL import Image, ImageDraw, ImageFont

class OledNode(Node):
    WIDTH = 128
    HEIGHT = 32

    def __init__(self):
        super().__init__(name=__name__)
    
    def start(self): 
        super().start()

        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.oled = adafruit_ssd1306.SSD1306_I2C(self.WIDTH, self.HEIGHT, i2c)
        except:
            self.warning("Failed to access OLED Display")
            self.stop()
            return
                    
        self.font = ImageFont.truetype("arial.ttf",8.8)
        self.image = Image.new("1", (self.WIDTH, self.HEIGHT))
        self.display_text("Hello from ai-robot")
        self.node_event_channel.subscribe("system-status", self.status_update)

    def status_update(self, status):
        self.display_text(f"""CPU Load: {status.cpu_load}%, Temp: {status.cpu_temp}{chr(176)}C
Disk: {status.disk_space_used} / {status.disk_space_total}Mb
Memory: {status.memory_used} / {status.memory_total}Mb""")
        
    def clear_display(self):
        self.oled.fill(0)
        self.oled.show()
        
    def display_text(self, text):
        draw = ImageDraw.Draw(self.image)
        draw.rectangle((0, 0, self.WIDTH, self.HEIGHT), outline=0, fill=0)
        draw.text( (0, 0), text, font=self.font, fill=255)

        self.oled.image(self.image)
        self.oled.show()

