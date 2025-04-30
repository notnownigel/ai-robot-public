from lancedb.pydantic import LanceModel, Vector
import uuid
import numpy as np
from typing import List, Dict

class FaceRecognitionSchema(LanceModel):
    id: str  # Unique identifier for each entry
    vector: Vector(512)  # type: ignore # Face embeddings, fixed size of 512
    entity_name: str  # Name of the entity

    @classmethod
    def prepare_face_records(cls, face_embeddings: List[Dict], entity_name: str) -> List['FaceRecognitionSchema']:
        """
        Converts a list of face detection results to a list of FaceRecognitionSchema instances.

        Args:
            face_embeddings (List[Dict]): List of face embeddings.
            entity_name (str): Name of the entity.

        Returns:
            List[FaceRecognitionSchema]: List of formatted instances.
        """
        if not face_embeddings:
            return []

        formatted_records = []
        for embedding in face_embeddings:
            formatted_records.append(
                cls(
                    id=str(uuid.uuid4()),  # Generate a unique ID
                    vector=np.array(embedding, dtype=np.float32),  # Convert embedding to float32 numpy array
                    entity_name=entity_name
                )
            )
        return formatted_records
