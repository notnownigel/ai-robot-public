# Robot Entry Point
import dotenv
from nodes import Ubermensch, FaceRecognition, PersonNode, StatusNode, MotionNode 
from nodes import DisplayNode, SpeechNode, BuzzerNode, OledNode, ServoNode, MotorNode, UPSNode

dotenv.load_dotenv()

# Run until Ctrl+Z pressed or system alarm
Ubermensch(
    UPSNode(),
    StatusNode(),
    FaceRecognition("./faces.db"),
    PersonNode(),
    SpeechNode(),
    MotionNode(),
    OledNode(),
    ServoNode(),
    MotorNode(),
    BuzzerNode(),
    DisplayNode()
)
