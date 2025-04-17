import degirum as dg
import degirum_tools
import numpy as np
from core import helpers

# Face AI class
class FaceAI:
    def __init__(self):
        # Face AI Modle
        self.zoo = dg.connect(dg.LOCAL, degirum_tools.get_cloud_zoo_url(), degirum_tools.get_token())

        # Face detection model
        self.face_det_model = self.zoo.load_model("scrfd_10g--640x640_quant_hailort_hailo8_1") 

        # Face recognition model
        self.face_rec_model =  self.zoo.load_model("arcface_mobilefacenet--112x112_quant_hailort_hailo8_1") 

        #self.model = degirum_tools.CroppingAndClassifyingCompoundModel(self.face_det_model, self.face_rec_model, 112.0)


    def get_faces_from_inference_result(self, result) -> list:
        images = []
        for face in result.results:
            x1, y1, x2, y2 = map(int, face["bbox"])
            face_img = result.image[y1:y2, x1:x2]
            images.append(face_img)
        return images
       
    def get_aligned_faces_from_inference_result(self, result) -> list:

        images = []
        for face in result.results:
            landmarks = [landmark["landmark"] for landmark in face["landmarks"]]
            aligned_face, _ = helpers.align_and_crop(result.image, landmarks)  # Align and crop face
            images.append(aligned_face)
        return images

    def detect_faces(self, frame: np.ndarray):
            return self.face_det_model.predict(frame)

    def get_face_embeddings(self, faces) -> list:

        results = self.face_rec_model.predict_batch(faces)
        embeddings = []

        for face_embedding in results:
            embeddings.append(face_embedding.results[0]["data"][0])
        return embeddings
