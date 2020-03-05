import os
import csv
import xml.etree.ElementTree as ET

ANNOTATIONS_DIR = "data/weapon/bbox"
IMAGES_DIR = "data/weapon/imgs/"
IMAGE_EXT = ".jpg"
ANNOTATION_FILE = "data/weapon/weapons.csv"

class Annotation():
    def __init__(self, imgpath, imgclass, bbox):
        self.filepath = imgpath
        self.imgclass = imgclass
        self.xmin = bbox['xmin']
        self.ymin = bbox['ymin']
        self.xmax = bbox['xmax']
        self.ymax = bbox['ymax']

def getAnnotations(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()

    annotations = []
    imgfile = None
    if root.tag == 'annotation':
        for child in root:
            if child.tag == 'filename':
                imgfile = child.text
            elif child.tag == 'object':
                bbox = {}
                for detail in child:
                    if detail.tag == 'name':
                        imgclass = detail.text
                    elif detail.tag == 'bndbox':
                        for corner in detail:
                            bbox[corner.tag] = corner.text
                if imgfile is None:
                    print(xmlFile+": FORMAT ERROR")
                else:
                    annotations.append(Annotation(imgfile, imgclass, bbox))
    return annotations

with open(ANNOTATION_FILE, "w", newline="") as annf:
    ann_writer = csv.writer(annf)
    for annfile in os.listdir(ANNOTATIONS_DIR):
        annotations = getAnnotations(ANNOTATIONS_DIR+'/'+annfile)
        for annotation in annotations:
            ann_writer.writerow([IMAGES_DIR+annotation.filepath+IMAGE_EXT, annotation.xmin, annotation.ymin, annotation.xmax, annotation.ymax, annotation.imgclass])
