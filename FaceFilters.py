# Import packages
import numpy as np
import dlib
import cv2

class FaceFilters:
    def __init__(self, filters):
        self.shape_predictor = 'shape_predictor_68_face_landmarks.dat'
        self.face_detector = dlib.get_frontal_face_detector()
        self.face_predictor = dlib.shape_predictor(self.shape_predictor)
        self.filters = filters

    def applyFilter(self, image, ft):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = self.face_detector(image,1)
    
        # loop over the face detections
        for rect in rects:
            shape = self.face_predictor(gray, rect)
            shape = self.shape_to_np(shape)
            
            filter_img = cv2.imread('filters/'+self.filters[ft], -1)
            filter_img2gray = cv2.cvtColor(filter_img, cv2.COLOR_BGR2GRAY)
            #retn, orig_mask = cv2.threshold(filter_img2gray, 60, 255, cv2.THRESH_BINARY)
            orig_mask = filter_img[:,:,3]
            orig_mask_inv = cv2.bitwise_not(orig_mask)
            filter_img = filter_img[:,:,0:3]
            origH, origW = filter_img.shape[:2]
            
            y1, y2, x1, x2, filters, filterW, filterH = self.face_filters(origW, origH, shape, filter_img, ft)
            roi = image[y1:y2, x1:x2]
            
            mask = cv2.resize(orig_mask, (filterW,filterH), interpolation = cv2.INTER_AREA)
            mask_inv = cv2.resize(orig_mask_inv, (filterW,filterH), interpolation = cv2.INTER_AREA)
            
            roi_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
            roi_fg = cv2.bitwise_and(filters,filters,mask = mask)
            dst = cv2.add(roi_bg, roi_fg)
            image[y1:y2, x1:x2] = dst

        return image

    def shape_to_np(self, shape, dtype='int'):
        # initialize the list of (x,y) coordinates
        coords = np.zeros((shape.num_parts, 2), dtype=dtype)
        for i in range(0, shape.num_parts):
            coords[i] = (shape.part(i).x, shape.part(i).y)
        
        # return x, y coordinates
        return coords

    def face_filters(self, origW, origH, shape, filter_img, choice):
    
        # realted only to eyes
        # sunglasses filter
        if choice >= 0 and choice <= 4:
            filterW = abs(int((shape[16][0] - shape[1][0])*1.1))
            filterH = int(filterW * origH / origW)
                
            y1 = int(shape[19][1])
            y2 = int(y1 + filterH)
            x1 = int(shape[27][0] - (filterW/2))
            x2 = int(x1 + filterW)
            
        # dog filter
        elif choice >= 5 and choice <= 6:
            filterW = abs(int((shape[16][0] - shape[1][0])*1.5))
            filterH = int((shape[58][1] - shape[20][1])*1.5)
        
            y2 = int(shape[52][1])
            y1 = int(y2 - filterH)
            x1 = int(shape[27][0]- (filterW/2))
            x2 = int(x1 + filterW)
            
        # rabbit filter
        elif choice == 7:
            filterW = abs(int((shape[16][0] - shape[1][0])*1.5))
            filterH = int((shape[58][1] - shape[20][1])*2)
            
            y2 = int(shape[67][1])
            y1 = int(y2 - filterH)
            x1 = int(shape[27][0]- (filterW/2))
            x2 = int(x1 + filterW)
            
        # moustache filter
        elif choice == 8 or choice == 9:
            filterW = abs(shape[16][0] - shape[1][0])
            filterH = int((shape[63][1] - shape[34][1])*1.5)
            
            y1 = int(shape[34][1])
            y2 = int(y1 + filterH)
            x1 = int(shape[27][0]- (filterW/2))
            x2 = int(x1 + filterW)
            
        # ironman/ spiderman mask filter
        elif choice == 10 or choice == 11:
            filterW = abs(int((shape[16][0] - shape[1][0])*1.5))
            filterH = int((shape[9][1] - shape[20][1])*1.8)
            
            y2 = int(shape[9][1] + 5)
            y1 = int(y2 - filterH)
            x1 = int(shape[27][0]- (filterW/2))
            x2 = int(x1 + filterW)
            
        # captain america/ batman mask
        elif choice == 12 or choice == 13:
            filterW = abs(int((shape[16][0] - shape[1][0])*1.2))
            filterH = int((shape[58][1] - shape[20][1])*1.8)
            
            y2 = int(shape[52][1])
            y1 = int(y2 - filterH)
            x1 = int(shape[27][0]- (filterW/2))
            x2 = int(x1 + filterW)
            
        filters = cv2.resize(filter_img, (filterW, filterH), interpolation = cv2.INTER_AREA)
        
        return y1, y2, x1, x2, filters, filterW, filterH