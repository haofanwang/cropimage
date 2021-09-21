import os
import cv2
import numpy as np
from PIL import Image

import torch
from facenet_pytorch import MTCNN

from .constants import *


class Cropper:
    
    def __init__(self, device='cpu'):
        self.DEVICE = torch.device(device)
        self.MTCNN_MODEL = MTCNN(keep_all=False, device=self.DEVICE)

    '''
    MTCNN is a famous face detection method that works well for multi-scale and profile face detection. For image crop, this method should enough for accuracy and efficiency.
    '''
    def center_from_mtcnn(self, image, face_number=1, face_threshold=0.95, area_threshold=0.002):

        height, width, channel = image.shape

        boxes, scores = self.MTCNN_MODEL.detect(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))

        cx, cy = 0, 0
        if boxes is not None and np.sum(np.array(scores)>face_threshold) == face_number:
            if face_number == 1:
                bbox = boxes[list(scores).index(scores.max())]
                if (bbox[2]-bbox[0])*(bbox[3]-bbox[1]) / (height*width) > area_threshold:
                    cx, cy = (int(bbox[2])+int(bbox[0]))//2, (int(bbox[3])+int(bbox[1]))//2
                    return (cx/face_number, cy/face_number, bbox)
                else:
                    return False
            # Not support well
            else:
                flag = False
                for i in range(len(boxes)):
                    bbox = boxes[i]
                    if scores[i] > face_threshold:
                        if (bbox[2]-bbox[0])*(bbox[3]-bbox[1]) / (height*width) > area_threshold:
                            cx += (int(bbox[2])+int(bbox[0]))//2
                            cy += (int(bbox[3])+int(bbox[1]))//2
                            if not flag:
                                flag = True
                if flag:
                    return (cx/face_number, cy/face_number)
                else:
                    return False
        else:
            return False

    '''
    Coarse face detection. This only works fine for large size face.
    '''
    def center_from_faces(self, image):

        # Front face detection
        face_cascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__),HAARCASCADE_FRONTALFACE))
        faces = face_cascade.detectMultiScale(image, FACE_DETECT_REJECT_LEVELS, 
                                              FACE_DETECT_LEVEL_WEIGHTS)

        # Profile face detection
        if len(faces) == 0:
            face_cascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__),HAARCASCADE_PROFILEFACE))
            faces = face_cascade.detectMultiScale(image, FACE_DETECT_REJECT_LEVELS, 
                                                  FACE_DETECT_LEVEL_WEIGHTS)

        if len(faces) == 0:
            return False

        weight = 0
        x, y = (0, 0)
        for (x, y, w, h) in faces:
            weight += w * h
            x += (x + w / 2) * w * h
            y += (y + h / 2) * w * h

        return {'x': x / weight, 'y': y / weight, 'count': len(faces)}

    '''
    Corner detection.
    '''
    def center_from_good_features(self, image):

        corners = cv2.goodFeaturesToTrack(image, 
                                          FEATURE_DETECT_MAX_CORNERS, 
                                          FEATURE_DETECT_QUALITY_LEVEL,
                                          FEATURE_DETECT_MIN_DISTANCE)
        weight = 0
        x, y = (0, 0)
        for point in corners:
            weight += 1
            x += point[0][0]
            y += point[0][1]

        return {'x': x / weight, 'y': y / weight, 'count': weight}

    '''
    Saliency detection for those pictures that do not have faces as main body.
    '''
    def center_from_saliency(self, image, save_saliency=False, save_dir='./'):

        # saliency detection
        saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
        (success, saliencyMap) = saliency.computeSaliency(image)
        saliencyMap = (saliencyMap * 255).astype("uint8")

        if save_saliency:
            cv2.imwrite(os.path.join(save_dir, image_name[:-4]+'_saliency.png'), saliencyMap)

        # find maximum point
        saliencyMap = np.array(saliencyMap)
        maximum_y, maximum_x = np.argwhere(saliencyMap==saliencyMap.max())[0]

        return maximum_x, maximum_y

    '''
    Detect the main body from given image
    '''
    def detect(self, image):

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        face_mtcnn = self.center_from_mtcnn(image)

        if face_mtcnn:
            cx, cy, bbox = face_mtcnn
        else:
            face_center = self.center_from_faces(gray)

            center = {'x': 0, 'y': 0}
            if not face_center:
                center_features = self.center_from_good_features(gray)
                center_saliency = self.center_from_saliency(image)
                center['x'] = (center_features['x']+center_saliency[0]) // 2
                center['y'] = (center_features['y']+center_saliency[1]) // 2
            else:
                features_center = self.center_from_good_features(gray)
                face_w = features_center['count'] * COMBINE_FACE_WEIGHT
                feat_w = features_center['count'] * COMBINE_FEATURE_WEIGHT
                center['x'] = (face_center['x'] * face_w + features_center['x'] * feat_w) / (face_w + feat_w)
                center['y'] = (face_center['y'] * face_w + features_center['y'] * feat_w) / (face_w + feat_w)
            cx, cy = int(center['x']), int(center['y'])
        return cx, cy, face_mtcnn 

    '''
    Detect and Crop the region
    '''
    def crop(self, image_dir, completeness=False, target_size=(500,500)):

        # read image
        image = cv2.imread(image_dir)
        height, width, channel= image.shape

        # the shape of image, horizontal or portrait
        ratio = width / height

        # center of the key region
        maximum_x, maximum_y, flag = self.detect(image)

        if ratio > HORIZONTAL_THRESHOLD:

            if flag and completeness:
                bbox = flag[-1]
                left_y = max(0,bbox[1]-height/8)
                right_y = min(height,bbox[3]+height/8)
                left_x, right_x = maximum_x-(right_y-left_y)//2, maximum_x+(right_y-left_y)//2
            else:
                left_x, right_x = maximum_x-height//2, maximum_x+height//2
                left_y, right_y = 0, height

            if left_x < 0:
                left_x, right_x = 0, right_x+abs(left_x)

            if right_x > width:
                left_x, right_x = left_x-abs(right_x), width

        elif ratio < PORTRAIT_THRESHOLD:

            if flag and completeness:
                bbox = flag[-1]
                left_y = max(0,bbox[1]-height/8)
                right_y = min(height,bbox[3]+height/8)
                left_x, right_x = maximum_x-(right_y-left_y)//2, maximum_x+(right_y-left_y)//2
            else:
                left_x, right_x = 0, width
                left_y, right_y = maximum_y-width//2, maximum_y+width//2

            if left_y < 0:
                left_y, right_y = 0, right_y+abs(left_y)

            if right_y > height:
                left_y, right_y = left_y-abs(right_y), height

        # nearly square
        else:
            if ratio > 1:
                cx, cy = width//2, height//2
                left_x, right_x = cx - height//2, cx + height//2
                left_y, right_y = cy - height//2, cy + height//2
            else:
                cx, cy = width//2, height//2
                left_x, right_x = cx - width//2, cy + width//2
                left_y, right_y = cy - width//2, cy + width//2

        left_y, right_y,left_x, right_x = int(left_y), int(right_y), int(left_x), int(right_x)

        if target_size is not None:
            return cv2.resize(image[left_y:right_y, left_x:right_x, :], target_size)
        else:
            return image[left_y:right_y, left_x:right_x, :]   