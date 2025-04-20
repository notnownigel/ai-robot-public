from dataclasses import dataclass

@dataclass()
class CameraCommand(object):

    CAMERA_STOP=0
    CAMERA_CENTER=1
    CAMERA_GOTO=2
    CAMERA_RELATIVE=3
    CAMERA_ABSOLUTE=4

    action: int
    pos: tuple = (0,0)
    steps: int = 1
    duration: int = 1

