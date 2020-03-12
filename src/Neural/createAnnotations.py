"""
Convert YoloV3 format into bounding boxes for RetinaNet training.

YoloV3 annotation: label xfrac yfrac widthfrac, heightfrac

where the label is an integer and other values are float fractions.
xfrac and widthfrac are fractions of the total image width
yfrac and heightfrac are fractions of the total image height
and
(xfrac, yfrac) repseents the center of the bounding box, not the top left corner as expected

"""

import os
import csv
from PIL import Image

CLASS_NAME = { 0:  'gun', 1: 'pistol' }
ANNOTATION_FILE = "gun.csv"
IMAGE_DIR = "data/gundetection"

all_files = file_names = os.listdir(IMAGE_DIR)

# Open output file avoiding the extra carriage return in Windows
with open(ANNOTATION_FILE, "w", newline="") as annf:
    ann_writer = csv.writer(annf)
    for yoloFile in all_files:
        pieces = os.path.splitext(yoloFile)
        if pieces[1] == '.txt':
            imgfile = IMAGE_DIR + '/' + pieces[0] + ".jpg"
            img = Image.open(imgfile)
            width, height = img.size
            with open(IMAGE_DIR+'/'+yoloFile) as yf:
                for annline in yf.readlines():
                    ratios = [float(x) for x in annline.split() ]
                    label = int(ratios[0])
                    x = int(ratios[1]*width)
                    y =  int(ratios[2]*height)
                    xmin = x - int(ratios[3]*width/2)
                    ymin = y - int(ratios[4]*height/2)
                    xmax = x + int(ratios[3]*width/2)
                    ymax = y + int(ratios[4]*height/2)
                    '''
                    im1 = img.crop((xmin, ymin, xmax, ymax))
                    im1.show()
                    '''
                    if (xmax > xmin) and (ymax > ymin):
                        ann_writer.writerow([imgfile, xmin, ymin, xmax, ymax, CLASS_NAME[label]])
