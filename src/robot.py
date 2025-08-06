# Robot Entry Point
import dotenv
from nodes import Ubermensch, FaceRecognition, PersonNode, StatusNode, MotionNode, LLMNode 
from nodes import DisplayNode, SpeechNode, BuzzerNode, OledNode, ServoNode, MotorNode, UPSNode

dotenv.load_dotenv()

# Run until Ctrl+Z pressed or system alarm
Ubermensch(
    UPSNode(),
    StatusNode(),
    OledNode(),
    ServoNode(),
    MotorNode(),
    BuzzerNode(),
    LLMNode(),
    SpeechNode(),
    FaceRecognition("./faces.db"),
    PersonNode(),
    MotionNode(),
    DisplayNode()
)
