import cv2
import logging
import os
import numpy as np

def init_logger(logger: logging.Logger):
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        level = os.getenv("LOGLEVEL")

        match level:
            case 'DEBUG':
                logger.setLevel(logging.DEBUG)
                return
            case 'INFO':
                logger.setLevel(logging.INFO)
                return
            case 'WARNING':
                logger.setLevel(logging.WARNING)
                return
            case 'ERROR':
                logger.setLevel(logging.ERROR)
                return
            case 'CRITICAL':
                logger.setLevel(logging.CRITICAL)
                return

        logger.setLevel(logging.INFO)

#Overlay images from imgList with scaled width
def overlay_images(img, imgList, maxWidth=64, margin=4) -> np.ndarray:
    x_offset= y_offset = margin

    for overlay in imgList:
        _, im_w = overlay.shape[:2]
        scale = maxWidth/(im_w)   
        overlay = cv2.resize(overlay,None,fx=scale,fy=scale)
        x_end = x_offset + overlay.shape[1]
        y_end = y_offset + overlay.shape[0]

        img[y_offset:y_end,x_offset:x_end] = overlay
        x_offset += 74
    return img

def overlay_label(img, label, pt: cv2.typing.Point, clr: cv2.typing.Scalar, bck: cv2.typing.Scalar=None) -> np.ndarray:
    (w, _), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)

    # Prints the text.    
    if bck is not None:
        img = cv2.rectangle(img, (pt[0], pt[1] - 20), (pt[0] + w, pt[1]), bck, -1)
    
    img = cv2.putText(img, label, (pt[0], pt[1] - 5), cv2.FONT_HERSHEY_PLAIN, 1, clr, 1)
    return img


def align_and_crop(img, landmarks, image_size=112) -> tuple:
    # Define the reference keypoints used in ArcFace model, based on a typical facial landmark set.
    _arcface_ref_kps = np.array(
        [
            [38.2946, 51.6963],  # Left eye
            [73.5318, 51.5014],  # Right eye
            [56.0252, 71.7366],  # Nose
            [41.5493, 92.3655],  # Left mouth corner
            [70.7299, 92.2041],  # Right mouth corner
        ],
        dtype=np.float32,
    )

    # Ensure the input landmarks have exactly 5 points (as expected for face alignment)
    assert len(landmarks) == 5

    # Validate that image_size is divisible by either 112 or 128 (common image sizes for face recognition models)
    assert image_size % 112 == 0 or image_size % 128 == 0

    # Adjust the scaling factor (ratio) based on the desired image size (112 or 128)
    if image_size % 112 == 0:
        ratio = float(image_size) / 112.0
        diff_x = 0  # No horizontal shift for 112 scaling
    else:
        ratio = float(image_size) / 128.0
        diff_x = 8.0 * ratio  # Horizontal shift for 128 scaling

    # Apply the scaling and shifting to the reference keypoints
    dst = _arcface_ref_kps * ratio
    dst[:, 0] += diff_x  # Apply the horizontal shift

    # Estimate the similarity transformation matrix to align the landmarks with the reference keypoints
    M, inliers = cv2.estimateAffinePartial2D(np.array(landmarks), dst, ransacReprojThreshold=1000)
    assert np.all(inliers == True)

    # Apply the affine transformation to the input image to align the face
    aligned_img = cv2.warpAffine(img, M, (image_size, image_size), borderValue=0.0)

    return aligned_img, M
