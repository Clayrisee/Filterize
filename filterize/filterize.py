import cv2
import numpy as np
import dlib
import time
from math import hypot
import os

BASE_DIR = os.getcwd()
PRETRAIN_MODEL_DIR = os.path.join(BASE_DIR,'pretrain_model')
FILTER_NOSE_DIR = os.path.join(BASE_DIR,'filterize','filter_img')

class Filterize:
    def __init__(
      self, 
      k=7,
      pretrain_haarscascade=os.path.join(PRETRAIN_MODEL_DIR, 'haarcascade_frontalface_default.xml'),
      pretrain_cnn=os.path.join(PRETRAIN_MODEL_DIR,'mmod_human_face_detector.dat'),
      pretrain_dlib_shape_predictor=os.path.join(PRETRAIN_MODEL_DIR,'shape_predictor_68_face_landmarks.dat'),
               ):
        self.k = k
        self.pretrain_haarscascade = pretrain_haarscascade
        self.pretrain_cnn = pretrain_cnn
        self.pretrain_dlib_shape_predictor = pretrain_dlib_shape_predictor

    def _color_quantization(self, img):
    # Define input data for clustering
        data = np.float32(img).reshape((-1, 3))
        # Define criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        # Apply K-means clustering
        ret, label, center = cv2.kmeans(data, self.k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(img.shape)
        return result
  
    def _cascade_face_detector(self,image):
        face_cascade = cv2.CascadeClassifier(self.pretrain_haarscascade)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray_image, 1.5, 3)

        for (x,y,w,h) in faces:
            # Crop ke ROI
            cropped_img = image[(y-5):((y)+(h+10)), (x-5):((x-2)+(w+5))]
        return cropped_img
    
    def _convert_and_trim_bb(self, img, rect):
        startX = rect.left()
        startY= rect.top()
        endX = rect.right()
        endY = rect.bottom()

        startX = max(0, startX)
        startY = max(0, startY)
        endX = min(endX, img.shape[1])
        endY = min(endY, img.shape[0])

        w = endX - startX
        h = endY - startY

        return (startX, startY, w, h)
  
    def _cnn_face_detection(self, img):
        detector = dlib.cnn_face_detection_model_v1(self.pretrain_cnn)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = detector(rgb, 0)

        boxes = [self._convert_and_trim_bb(img, r.rect) for r in results]
        print(len(boxes))
        for (x, y, w, h) in boxes:
            cropped_img = img[(y-5):((y)+(h+10)), (x-5):((x-2)+(w+5))]
        
        return cropped_img

    def create_cartoon_img(self, img, method='cascade'):
        """
        img : path gambar yang ingin dilakukan kartunisasi
        method : pemilihan methode (cnn/cascade)
        """
        try:
            image = cv2.imread(img)
            if method == 'cascade':
                cropped_img = self._cascade_face_detector(image)
            elif method == 'cnn':
                cropped_img = self._cnn_face_detection(image)
            else:
                raise ValueError("Method not found, only(cnn/cascade)")

            segmented_img = self._color_quantization(cropped_img)
            # Create blur effect
            blurred = cv2.medianBlur(segmented_img, 3)
            gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
            # Detect Edges
            edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 5)
            finalized_img = cv2.bitwise_and(blurred, blurred, mask=edges)
            finalized_img = cv2.resize(finalized_img, (250, 250), interpolation = cv2.INTER_AREA)
            
        
        except NameError:
            print(NameError)
        return finalized_img
  
    def nose_filter(self, image, nose_filter='cat'):
        """
        image : path gambar yang ingin diproses
        nose_filter : jenis filter hidung yang ingin digunakan(pig, cat, dan dog)
        """
        img = cv2.imread(image)
        if nose_filter == 'pig':
            img_path = os.path.join(FILTER_NOSE_DIR, 'pig_nose.png')
            nose_img = cv2.imread(img_path)
        elif nose_filter == 'cat':
            img_path = os.path.join(FILTER_NOSE_DIR, 'cat_nose.png')
            nose_img = cv2.imread(img_path)
        elif nose_filter == 'dog':
            img_path = os.path.join(FILTER_NOSE_DIR, 'dog_nose.png')
            nose_img = cv2.imread(img_path)
        else:
            raise ValueError("Nose filter not found, please input only cat / pig")
        nose_mask = np.zeros(img.shape[:2], dtype='uint8')
        # Create ratio
        nose_ratio = (nose_img.shape[0] / nose_img.shape[1])
        # Load face landmark detector
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(self.pretrain_dlib_shape_predictor)
        nose_mask.fill(0)
        # convert img to gray 
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = detector(img)

        for face in faces:
            landmarks = predictor(gray_img, face)

            # Nose coordinate based on dlib  68 face landmarks
            top_nose = (landmarks.part(29).x, landmarks.part(29).y)
            center_nose = (landmarks.part(30).x, landmarks.part(30).y)
            left_nose = (landmarks.part(31).x, landmarks.part(31).y)
            right_nose =(landmarks.part(35).x, landmarks.part(35).y)

            # Get nose width and height
            if nose_filter == 'pig':
                nose_width = int(hypot(left_nose[0] - right_nose[0], left_nose[1] - right_nose[1]) * 2)
                nose_height = int(nose_width * nose_ratio)
            elif nose_filter == 'dog':
                nose_width = int(hypot(left_nose[0] - right_nose[0], left_nose[1] - right_nose[1]) * 4)
                nose_height = int(nose_width * nose_ratio)
            else:
                nose_width = int(hypot(left_nose[0] - right_nose[0], left_nose[1] - right_nose[1]) * 3)
                nose_height = int(nose_width * nose_ratio)
            

            # Get new nose position
            top_left = (int(center_nose[0] - nose_width / 2),
                        int(center_nose[1] - nose_height / 2))
            bottom_right = (int(center_nose[0] + nose_width / 2),
                        int(center_nose[1] + nose_height / 2))
            # Adding nose filter
            nose_img = cv2.resize(nose_img, (nose_width, nose_height))
            nose_img_gray = cv2.cvtColor(nose_img, cv2.COLOR_BGR2GRAY)

            # Create nose mask using tresholding
            _, nose_mask = cv2.threshold(nose_img_gray, 25, 255, cv2.THRESH_BINARY_INV)

            # create ROI
            nose_area = img[top_left[1]: top_left[1] + nose_height, top_left[0]: top_left[0] + nose_width]
            nose_area_no_nose = cv2.bitwise_and(nose_area, nose_area, mask=nose_mask)

            final_nose = cv2.add(nose_area_no_nose, nose_img)

            img[top_left[1]: top_left[1] + nose_height, top_left[0]: top_left[0] + nose_width] = final_nose
        
        return img

# def show_img(img):
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     plt.grid(None)
#     plt.grid(None)   
#     plt.xticks([])
#     plt.yticks([])
#     imgplot = plt.imshow(img)