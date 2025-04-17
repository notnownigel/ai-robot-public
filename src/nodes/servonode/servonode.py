import time
from typing import List
from core.i2cnode import I2CNode
from core import CameraCommand, Shared
from threading import Thread, Event

class ServoNode(I2CNode):
    def __init__(self):
        super().__init__(name=__name__, address=self.RASPBOT)

    def start(self): 
        super().start() 

        if self.running:       
            self.sequence = []
            self.stop_now = False
            self.node_event_channel.subscribe("servo-execute-sequence", self.execute_sequence)
            self.node_event_channel.subscribe("servo-command", self.execute)
            self.center()
            self.trigger = Event()
            Thread(target=self.run, daemon=True).start()
    
    def stop(self):
        self.stop_now = True
        super().stop()

    def run(self):
        while self.running:
            if self.trigger.wait(10):
                self.trigger.clear()
                
                while len(self.sequence):
                    self.execute(self.sequence.pop(0))

            self.stop_now = False

    def execute(self, command: CameraCommand):
        match command.action:
            case CameraCommand.CAMERA_CENTER:
                self.moveTo(Shared.SERVO_CENTER_X, Shared.SERVO_CENTER_Y, command.steps, command.duration)
            case CameraCommand.CAMERA_GOTO:
                self.moveTo(command.end_pos[0], command.end_pos[1], command.steps, command.duration)
            case CameraCommand.CAMERA_RELATIVE:
                self.position(Shared.servo_x+command.relative[0], Shared.servo_y+command.relative[1])
            case CameraCommand.CAMERA_STOP:
                if Shared.manual_mode is False:
                    self.stop_now = True

    def moveTo(self, x, y, steps, duration):
        delay = duration/steps
        delta_x = (x-Shared.servo_x)/steps
        delta_y = (y-Shared.servo_y)/steps

        for n in range(0, steps):
            self.position(Shared.servo_x+delta_x, Shared.servo_y+delta_y)
            time.sleep(delay)

    def center(self):
        self.position(Shared.SERVO_CENTER_X, Shared.SERVO_CENTER_Y)

    def position(self, x: int, y: int):
        if self.stop_now is False:
            if x >= Shared.SERVO_MIN_X and x <= Shared.SERVO_MAX_X: 
                self.write_array(I2CNode.RASPBOT_SERVO, [0x01, int(x)])
                Shared.servo_x = x
                
            if y >= Shared.SERVO_MIN_Y and y <= Shared.SERVO_MAX_Y: 
                self.write_array(I2CNode.RASPBOT_SERVO, [0x02, int(y)])
                Shared.servo_y = y

    def execute_sequence(self, sequence: List):
        self.sequence = sequence
        self.stop_now = False
        self.trigger.set()        
