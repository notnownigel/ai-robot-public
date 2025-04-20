from dataclasses import dataclass

@dataclass()
class Shared(object):
    # Motor Speed
    SPEED_STOP=0
    SPEED_STEP=1
    SPEED_SLOW=50
    SPEED_MEDIUM=100
    SPEED_FAST=200
    SPEED_LIGHTNING=255

    # Servo Range
    SERVO_MIN_X = 0
    SERVO_MIN_Y = 0
    SERVO_MAX_X = 180
    SERVO_MAX_Y = 120
    SERVO_CENTER_X = 90
    SERVO_CENTER_Y = 20

    # Servo current position
    servo_x = 0
    servo_y = 0
    
    # Screen Dimentions
    screen_width = 640
    screen_height = 480

    # Flags
    manual_mode = False

    # Nodes
    nodes = []
