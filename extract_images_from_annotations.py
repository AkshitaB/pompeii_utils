import os
import cv2
import ipdb
import numpy as np
import time
import glob
import math
import argparse

def extract(annotations_folder, output_folder):
    for anno in glob.glob(os.path.join(annotations_folder, 'page*.jpg')):
    #for anno in [os.path.join(annotations_folder, 'page_24.txt')]:
        page = os.path.basename(anno).split('.jpg')[0]
        for old_file in glob.glob(os.path.join(output_folder, page+'*')):
            os.remove(old_file)

    for anno in glob.glob(os.path.join(annotations_folder, 'page*.txt')):
    #for anno in [os.path.join(annotations_folder, 'page_24.txt')]:
        page = os.path.basename(anno).split('.txt')[0]
        raw_img = cv2.imread(os.path.join(annotations_folder, page+'.jpg'))
        height = raw_img.shape[0]
        width = raw_img.shape[1]
        
        #print(width)
        #print(height)

        with open(anno, 'r') as f:
            annotations = f.readlines()
            
            for idx, annotation in enumerate(annotations):
                annotation = annotation.replace('\n', '')
                tmp = annotation.split(' ')
                center_x = float(tmp[1])*width
                center_y = float(tmp[2])*height
                w = float(tmp[3])*width
                h = float(tmp[4])*height
                
                top_x = math.floor(center_x - (w / 2))
                top_y = math.floor(center_y - (h / 2))
                bottom_x = math.ceil(center_x + (w / 2))
                bottom_y = math.ceil(center_y + (h / 2))
                
                #print([top_x, top_y, bottom_x, bottom_y])
                
                roi = raw_img[top_y:bottom_y, top_x:bottom_x, :]
                #print(roi.shape)
                #print(os.path.join(output_folder, page+'_'+str(idx)+'.jpg'))
                cv2.imwrite(os.path.join(output_folder, page+'_'+str(idx)+'.jpg'), roi)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract pictures from annotations')
    parser.add_argument('annotations_folder', help='Path of folder with raw images and annotations')
    parser.add_argument('output_folder', help='Path of the folder where pictures will be extracted')

    args = parser.parse_args()

    extract(args.annotations_folder, args.output_folder)
