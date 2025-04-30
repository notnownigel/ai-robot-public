import logging
import numpy as np
from pathlib import Path
from typing import List, Any
from core import Storage, helpers, FaceRecognitionSchema

top_k = 1
field_name = "vector"
metric_type = "cosine"

class FaceStorage(Storage):

    def __init__(self, uri, table, schema):
        super().__init__(uri, table, schema)
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        self.logger = logger

    def populate_database_from_images(self, input_path: str, face_det_model: Any, face_rec_model: Any) -> None:

        path = Path(input_path)
        num_entities = 0  # Counter for the number of entities added to the database

        # Find all image files in the directory and subdirectories
        image_files = [str(file) for file in path.rglob("*") if file.suffix.lower() in (".png", ".jpg", ".jpeg")]
        identities = [file.stem.split("_")[0] for file in path.rglob("*") if file.suffix.lower() in (".png", ".jpg", ".jpeg")]
    
        if not image_files:
            logging.warning(f"No image files found in {input_path}.")
            return

        for identity, detected_faces in zip(identities, face_det_model.predict_batch(image_files)):
            try:
                print(identity, detected_faces.info)
                # Count number of detected faces
                num_faces = len(detected_faces.results)

                # Skip images with more than one face
                if num_faces > 1:
                    logging.warning(f"Skipped {detected_faces.info} as it contains more than one face ({num_faces} faces detected).")
                    continue
                elif num_faces == 0:
                    logging.warning(f"Skipped {detected_faces.info} as no faces were detected.")
                    continue

                # Process the single detected face
                result = detected_faces.results[0]

                # Generate face embedding
                aligned_img, _ = helpers.align_and_crop(detected_faces.image, [landmark["landmark"] for landmark in result["landmarks"]])
                face_embedding = face_rec_model(aligned_img).results[0]["data"][0]
                
                # Prepare records for the database
                records = FaceRecognitionSchema.prepare_face_records([face_embedding], identity)

                # Add records to the database if valid
                if records:
                    self.table.add(data=records)
                    num_entities += len(records)
                else:
                    logging.warning(f"No valid records generated for {detected_faces.info}.")

            except Exception as e:
                logging.error(f"Error processing file: {e}", exc_info=True)

        # Log summary
        logging.info(f"Successfully added {num_entities} entities to the database table.")
        total_entities = self.table.count_rows()
        logging.info(f"The table now contains {total_entities} entities.")

    def identify_faces(self, embeddings: List[np.ndarray], threshold: float = 0.3) -> List[str]:
        identities = []  # List to store the assigned labels
        similarity_scores = []  # List to store the similarity scores

        for embedding in embeddings:
            # Perform database search
            search_result = (
                self.table.search(
                    embedding,
                    vector_column_name=field_name
                )
                .metric(metric_type)
                .limit(top_k)
                .to_list()
            )

            # Check if search_result has any entries
            if not search_result:
                identities.append("")
                continue

            # Calculate the similarity score
            similarity_score = round(1 - search_result[0]["_distance"], 2)

            # Assign a label based on the similarity threshold
            identity = search_result[0]["entity_name"] if similarity_score >= threshold else ""

            # Append the label to the results list
            identities.append(identity)
            similarity_scores.append(similarity_score)
        return identities, similarity_scores
    