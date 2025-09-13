# DatabSE Generator
from nodes import FaceStorage, FaceAI 
from core import FaceRecognitionSchema 

ai = FaceAI()
db = FaceStorage("./faces.db", "faces", FaceRecognitionSchema)
db.populate_database_from_images(input_path="./assets/known", face_det_model=ai.face_det_model, face_rec_model=ai.face_rec_model)
