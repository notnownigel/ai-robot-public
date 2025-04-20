from core import Node, CameraCommand, Shared, Thing
from typing import List

# This class controls motion and includes the definition of these motions
# Calls servo and motor classes to execute a motion 

class MotionNode(Node):
    def __init__(self):
        super().__init__(name=__name__)
    
    def start(self): 
        super().start()
        self.node_event_channel.subscribe("start-looking-around", self.start_looking_around)
        self.node_event_channel.subscribe("stop-looking-around", self.stop_looking_around)
        self.node_event_channel.subscribe("centre-thing", self.centre_thing)
    
    def start_looking_around(self):
        self.info(f"Start looking around.")        
        self.node_event_channel.publish("servo-execute-sequence", self.looking_around_sequence())

    def stop_looking_around(self):
        self.node_event_channel.publish("servo-command", CameraCommand(action=CameraCommand.CAMERA_STOP))

    def centre_thing(self,  thing: Thing):
        # To Centre:
        #   y -> use camera 
        #   x -> use rotation then camera 
        
        xoffset = thing.offset[0]
        yoffset = thing.offset[1]
        yratio = ((Shared.screen_height/2)-yoffset) / Shared.screen_height

        if yratio < 0.5:
            self.node_event_channel.publish("servo-command", CameraCommand(action=CameraCommand.CAMERA_ABSOLUTE, pos=(Shared.servo_x, Shared.servo_y-2)))
        if yratio > 0.6:
            self.node_event_channel.publish("servo-command", CameraCommand(action=CameraCommand.CAMERA_ABSOLUTE, pos=(Shared.servo_x, Shared.servo_y+2)))
        pass

    def looking_around_sequence(self) -> List:
        return [
            CameraCommand(action=CameraCommand.CAMERA_GOTO, pos=(Shared.SERVO_MIN_X, Shared.SERVO_MAX_Y), steps=40, duration=4),
            CameraCommand(action=CameraCommand.CAMERA_CENTER, steps=40, duration=4),
            CameraCommand(action=CameraCommand.CAMERA_GOTO, pos=(Shared.SERVO_MAX_X, Shared.SERVO_MAX_Y), steps=40, duration=4),
            CameraCommand(action=CameraCommand.CAMERA_CENTER, steps=40, duration=4),
            CameraCommand(action=CameraCommand.CAMERA_GOTO, pos=(Shared.SERVO_MIN_X, Shared.SERVO_MIN_Y), steps=40, duration=4),
            CameraCommand(action=CameraCommand.CAMERA_CENTER, steps=40, duration=4),
            CameraCommand(action=CameraCommand.CAMERA_GOTO, pos=(Shared.SERVO_MAX_X, Shared.SERVO_MIN_Y), steps=40, duration=4),
            CameraCommand(action=CameraCommand.CAMERA_CENTER, steps=40, duration=4)
        ]
