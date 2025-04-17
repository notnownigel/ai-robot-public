import os
from threading import Thread
from core.node import Node
from .camerastream import CameraStream 
from .hailoface import FaceAI
from .schemas import FaceRecognitionSchema
from .facestorage import FactoryStorage
from core import Person, helpers

class FaceRecognition(Node):
    def __init__(self, dbpath):
        super().__init__(name=__name__)
        self.dbpath = dbpath

    def generate_db(self, assets):
        self.db.populate_database_from_images(
            input_path = assets,
            face_det_model = self.ai.face_det_model,
            face_rec_model = self.ai.face_rec_model
        )

    def start(self): 
        super().start()
        self.camera = CameraStream("camera")
        self.camera.start()
        self.db = FactoryStorage(self.dbpath, "faces", FaceRecognitionSchema)
        self.ai = FaceAI()
        Thread(target=self.run, daemon=True).start()
        
    def run(self):
        for frame in self.camera.frame_generator():

            # Detect faces and get aligned faces
            result = self.ai.detect_faces(frame)
            faces = self.ai.get_aligned_faces_from_inference_result(result)

            # Run batch predict on aligned faces, find identity, assign labels and scores to each detection
            for face, face_embedding in zip(result.results, self.ai.get_face_embeddings(faces)):
                identities, similarity_scores = self.db.identify_faces([face_embedding])
                face["label"] = identities[0]  # Assign the first label
                face["score"] = similarity_scores[0]  # Assign the first score

            # Display frame
            for face in result.results:
                name = face["label"]

                if name != "":
                    x1, y1, x2, y2 = map(int, face["bbox"])  # Convert bbox coordinates to integers
                    frame = helpers.overlay_label(frame, name, (x1, y1), (255,255,255), (255,0,0))
                    # concert bbox to rectangle relative to frame center
                    height, width = frame.shape[:2]

                    # get person score
                    person_score = os.getenv(f"PERSON_SCORE_{name.upper()}")
                    person_score = 5 if person_score is None else person_score
                    self.node_event_channel.publish("person-detected", Person(name=name, match_score=float(face["score"]), bbox=(x1, y1, x2, y2), offset=(int(x2-x1-(width/2)), int(y2-y1-(height/2))), person_score=person_score))

            self.node_event_channel.publish("display-node-frame", frame)
        
            # Are we still running?
            if self.running is False:
                self.camera.stop()
                break
