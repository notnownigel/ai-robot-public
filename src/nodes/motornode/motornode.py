import time
from core import Shared
from core.i2cnode import I2CNode

class MotorNode(I2CNode):
    WHEEL_LEFT_FRONT = 0
    WHEEL_LEFT_BACK = 1
    WHEEL_RIGHT_FRONT = 2
    WHEEL_RIGHT_BACK = 3

    DIRECTION_FORWARDS = 0
    DIRECTION_BACKWARDS = 1

    def __init__(self):
        super().__init__(name=__name__, address=self.RASPBOT)

    def start(self): 
        super().start()  
        self.node_event_channel.subscribe("motor-stop", self.stop_drive)
        self.node_event_channel.subscribe("motor-forwards", self.forwards)
        self.node_event_channel.subscribe("motor-backwards", self.backwards)
        self.node_event_channel.subscribe("motor-pan-left", self.pan_left)
        self.node_event_channel.subscribe("motor-pan-right", self.pan_right)
        self.node_event_channel.subscribe("motor-translate-forward-left", self.translate_forward_left)
        self.node_event_channel.subscribe("motor-translate-forward-right", self.translate_forward_right)
        self.node_event_channel.subscribe("motor-translate-back-left", self.translate_back_left)
        self.node_event_channel.subscribe("motor-translate-back-right", self.translate_back_right)
        self.node_event_channel.subscribe("motor-rotate-left", self.rotate_left)
        self.node_event_channel.subscribe("motor-rotate-right", self.rotate_right)
    
    def forwards(self, speed: int, duration: float):
        self.drive(MotorNode.WHEEL_LEFT_FRONT, MotorNode.DIRECTION_FORWARDS, speed)
        self.drive(MotorNode.WHEEL_RIGHT_FRONT, MotorNode.DIRECTION_FORWARDS, speed)
        self.drive(MotorNode.WHEEL_LEFT_BACK, MotorNode.DIRECTION_FORWARDS, speed)
        self.drive(MotorNode.WHEEL_RIGHT_BACK, MotorNode.DIRECTION_FORWARDS, speed)
        time.sleep(duration)
        self.stop_drive()

    def backwards(self, speed: int, duration: float):
        self.drive(MotorNode.WHEEL_LEFT_FRONT, MotorNode.DIRECTION_BACKWARDS, speed)
        self.drive(MotorNode.WHEEL_RIGHT_FRONT, MotorNode.DIRECTION_BACKWARDS, speed)
        self.drive(MotorNode.WHEEL_LEFT_BACK, MotorNode.DIRECTION_BACKWARDS, speed)
        self.drive(MotorNode.WHEEL_RIGHT_BACK, MotorNode.DIRECTION_BACKWARDS, speed)
        time.sleep(duration)
        self.stop_drive()

    def pan_left(self, speed: int, duration: float):
        self.drive(MotorNode.WHEEL_LEFT_FRONT, MotorNode.DIRECTION_BACKWARDS, speed)
        self.drive(MotorNode.WHEEL_RIGHT_FRONT, MotorNode.DIRECTION_FORWARDS, speed)
        self.drive(MotorNode.WHEEL_LEFT_BACK, MotorNode.DIRECTION_FORWARDS, speed)
        self.drive(MotorNode.WHEEL_RIGHT_BACK, MotorNode.DIRECTION_BACKWARDS, speed)
        time.sleep(duration)
        self.stop_drive()

    def pan_right(self, speed: int, duration: float):
        self.drive(MotorNode.WHEEL_LEFT_FRONT, MotorNode.DIRECTION_FORWARDS, speed)
        self.drive(MotorNode.WHEEL_RIGHT_FRONT, MotorNode.DIRECTION_BACKWARDS, speed)
        self.drive(MotorNode.WHEEL_LEFT_BACK, MotorNode.DIRECTION_BACKWARDS, speed)
        self.drive(MotorNode.WHEEL_RIGHT_BACK, MotorNode.DIRECTION_FORWARDS, speed)
        time.sleep(duration)
        self.stop_drive()

    def translate_forward_left(self, speed: int, duration: float):
        self.drive(MotorNode.WHEEL_RIGHT_FRONT, MotorNode.DIRECTION_FORWARDS, speed)
        self.drive(MotorNode.WHEEL_LEFT_BACK, MotorNode.DIRECTION_FORWARDS, speed)
        time.sleep(duration)
        self.stop_drive()

    def translate_forward_right(self, speed: int, duration: float):
        self.drive(MotorNode.WHEEL_LEFT_FRONT, MotorNode.DIRECTION_FORWARDS, speed)
        self.drive(MotorNode.WHEEL_RIGHT_BACK, MotorNode.DIRECTION_FORWARDS, speed)
        time.sleep(duration)
        self.stop_drive()

    def translate_back_left(self, speed: int, duration: float):
        self.drive(MotorNode.WHEEL_LEFT_FRONT, MotorNode.DIRECTION_BACKWARDS, speed)
        self.drive(MotorNode.WHEEL_RIGHT_BACK, MotorNode.DIRECTION_BACKWARDS, speed)
        time.sleep(duration)
        self.stop_drive()

    def translate_back_right(self, speed: int, duration: float):
        self.drive(MotorNode.WHEEL_RIGHT_FRONT, MotorNode.DIRECTION_BACKWARDS, speed)
        self.drive(MotorNode.WHEEL_LEFT_BACK, MotorNode.DIRECTION_BACKWARDS, speed)
        time.sleep(duration)
        self.stop_drive()

    def rotate_left(self, speed: int, duration: float):
        self.drive(MotorNode.WHEEL_LEFT_FRONT, MotorNode.DIRECTION_BACKWARDS, speed)
        self.drive(MotorNode.WHEEL_RIGHT_FRONT, MotorNode.DIRECTION_FORWARDS, speed)
        self.drive(MotorNode.WHEEL_LEFT_BACK, MotorNode.DIRECTION_BACKWARDS, speed)
        self.drive(MotorNode.WHEEL_RIGHT_BACK, MotorNode.DIRECTION_FORWARDS, speed)
        time.sleep(duration)
        self.stop_drive()

    def rotate_right(self, speed: int, duration: float):
        self.drive(MotorNode.WHEEL_LEFT_FRONT, MotorNode.DIRECTION_FORWARDS, speed)
        self.drive(MotorNode.WHEEL_RIGHT_FRONT, MotorNode.DIRECTION_BACKWARDS, speed)
        self.drive(MotorNode.WHEEL_LEFT_BACK, MotorNode.DIRECTION_FORWARDS, speed)
        self.drive(MotorNode.WHEEL_RIGHT_BACK, MotorNode.DIRECTION_BACKWARDS, speed)
        time.sleep(duration)
        self.stop_drive()

    def stop_drive(self):
        self.drive(MotorNode.WHEEL_LEFT_FRONT, MotorNode.DIRECTION_FORWARDS, Shared.SPEED_STOP)
        self.drive(MotorNode.WHEEL_RIGHT_FRONT, MotorNode.DIRECTION_FORWARDS, Shared.SPEED_STOP)
        self.drive(MotorNode.WHEEL_LEFT_BACK, MotorNode.DIRECTION_FORWARDS, Shared.SPEED_STOP)
        self.drive(MotorNode.WHEEL_RIGHT_BACK, MotorNode.DIRECTION_FORWARDS, Shared.SPEED_STOP)

    def drive(self, motor: int, direction: int, speed: int):
        self.write_array(I2CNode.RASPBOT_MOTOR, [motor, direction, speed])

