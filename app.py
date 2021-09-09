from filterize.filterize import Filterize
from filterize.filterize import show_img
import cv2
import os
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i','--image', type=str, required=True,help="path to input image")
ap.add_argument('-f', '--filter', type=str, required=True, help="choose filter mode [cartoon/nose_filter]")
ap.add_argument('-n', '--nose', type=str, required=True, help="choose nose filter mode [cat/pig/dog]")
args= vars(ap.parse_args())

filterize = Filterize()
print(args['image'])
try:
    img = cv2.imread(args['image'])
except NameError:
    print(NameError)
cv2.imshow("BEFORE", cv2.imread(args['image']))
if args['filter'] == 'cartoon':
    cartoon_img = filterize.create_cartoon_img(args['image'])
    cv2.imshow("Hasil Filter", cartoon_img)
else:
    filter_img = filterize.nose_filter(args['image'], args['nose'])
    cv2.imshow("Hasil Filter", filter_img)

cv2.waitKey(0) & 0xFF