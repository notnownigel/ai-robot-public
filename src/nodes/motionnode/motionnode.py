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
        xratio = ((Shared.screen_width/2)-xoffset) / Shared.screen_width
        yoffset = thing.offset[1]
        yratio = ((Shared.screen_height/2)-yoffset) / Shared.screen_height

        if xratio < 0.2:
            self.node_event_channel.publish("motor-rotate-right", Shared.SPEED_SLOW, 0.1)
            return

        if xratio > 0.7:
            self.node_event_channel.publish("motor-rotate-left", Shared.SPEED_SLOW, 0.1)
            return

        xPos = Shared.servo_x
        yPos = Shared.servo_y

        if yratio < 0.5:
            yPos = yPos - 2

        if yratio > 0.6:
            yPos = yPos + 2

        if xratio < 0.4:
            xPos = xPos - 2

        if xratio > 0.5:
            xPos = xPos + 2

        if xPos != Shared.servo_x or yPos != Shared.servo_y:
            self.node_event_channel.publish("servo-command", CameraCommand(action=CameraCommand.CAMERA_ABSOLUTE, pos=(xPos, yPos)))

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
