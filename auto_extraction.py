import os
import cv2
import ipdb
import numpy as np
import time
import glob
import argparse

class Point:
    def __init__(self, x, y): 
        self.x = x 
        self.y = y 

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)
    
def doOverlap(l1, r1, l2, r2): 
      
    # If one rectangle is on left side of other 
    if(l1.x > r2.x or l2.x > r1.x): 
        return False
  
    # If one rectangle is above other 
    if(l1.y > r2.y or l2.y > r1.y): 
        return False
  
    return True

def isBounding(l1, r1, l2, r2):

    def isInside(l1, r1, l2, r2):
        if l1.x < l2.x and r1.x > r2.x and l1.y < l2.y and r1.y > r2.y:
            return True
#         elif l1.x < l2.x and r1.x > l2.x and l1.y < l2.y and l2.y < r2.y:
#             return True
        elif doOverlap(l1, r1, l2, r2):
            return True
        return False

    if isInside(l1, r1, l2, r2):
        return 1
    elif isInside(l2, r2, l1, r1):
        return 2
    else:
        return 0

def get_rois(imgray, raw_image, page, output_folder):
    contours, hierarchy =  cv2.findContours(imgray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours]

    contours = sorted(contours, key=len, reverse=True)
    roiPoints = []

    for cnt in contours[:6]:
        x, y, w, h = cv2.boundingRect(cnt)
        if h == imgray.shape[0] and w == imgray.shape[1]:
            continue
            
        perc_area = (h*w)/(imgray.shape[0]*imgray.shape[1])
        
#         print(h*w)
#         print(imgray.shape[0]*imgray.shape[1])
        
        if h*w < 0.08*imgray.shape[0]*imgray.shape[1]:
            #print('size too small', perc_area)
            continue

        roi = imgray[y:y+h,x:x+w]

        flag = False
        for r in roiPoints:
            isBound = isBounding(r[0], r[1], Point(x, y), Point(x+w, y+h))
            if isBound == 1:
                flag = True
                break
            elif isBound == 2:
                flag = True
                r[0] = Point(x, y)
                r[1] = Point(x+w, y+h)
        if flag:
            #print('overlap')
            continue
        roiPoints.append([Point(x, y), Point(x+w, y+h)])
        
    roiPoints = sorted(roiPoints, key=lambda x:(x[1].y, x[1].x))

    for idx, roiPoint in enumerate(roiPoints):
        roi = raw_image[roiPoint[0].y:roiPoint[1].y, roiPoint[0].x:roiPoint[1].x]
        cv2.imwrite(os.path.join(output_folder, '{}_{}'.format(page, idx) + '.jpg'), roi)

def new_extract_images(raw_folder, output_folder):
    idx = 0
    #for img_path in glob.glob(os.path.join(raw_folder, '*.jpg')):
    for img_path in [os.path.join(raw_folder, x) for x in ['page_{}.jpg'.format(i) for i in range(32, 50)]]:
        #print(img_path)
        basename = os.path.basename(img_path)
        page = basename.split('.jpg')[0]
        #img = cv2.imread(img_path, 0)
        img = cv2.imread(os.path.join(raw_folder, basename), 0)
        raw_img = cv2.imread(os.path.join(raw_folder, basename))
        
        blur = cv2.GaussianBlur(img, (5, 5), 0)
        ret3, img = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        #cv2.imwrite(os.path.join(bin_image_folder, image), th3)
        
        #img = img[int(img.shape[1]*0.03):, :]
        #raw_img = raw_img[int(raw_img.shape[1]*0.03):, :]
        
        output = img
        
        kernel = np.ones((5, 5), np.uint8)
        kernel_small = np.ones((3, 3), np.uint8)
        
        #output = cv2.morphologyEx(output, cv2.MORPH_CLOSE, kernel, iterations=1)
        #output = cv2.erode(output, kernel, iterations=5)

        output = cv2.morphologyEx(output, cv2.MORPH_CLOSE, kernel, iterations=3)
        output = cv2.erode(output, kernel, iterations=5)
        
        #output = 255 - output
        #cv2.imwrite(os.path.join(output_folder, 'eroded_'+basename), output)
        
        get_rois(output, raw_img, page, output_folder)
        
        idx += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract pictures from PDF page images')
    parser.add_argument('raw_folder', help='Path of PDF page images')
    parser.add_argument('output_folder', help='Path of the folder where pictures will be extracted')

    args = parser.parse_args()

    new_extract_images(args.raw_folder, args.output_folder)
