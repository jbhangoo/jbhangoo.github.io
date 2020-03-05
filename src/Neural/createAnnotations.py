import os
import csv

CLASS_NAME = 'person'
ANNOTATION_FILE = "person.csv"
IMAGE_DIR = "data/person/WiderPerson/Images"
BBOX_DIR = "data/person/WiderPerson/Annotations"

bbox_files = file_names = os.listdir(BBOX_DIR)

# Open output file avoiding the extra carriage return in Windows
with open(ANNOTATION_FILE, "w", newline="") as annf:
    ann_writer = csv.writer(annf)
    for bbox_file in bbox_files:
        with open(BBOX_DIR+'/'+bbox_file) as bbf:
            next(bbf)
            for annline in bbf.readlines():
                bbox = annline.split()
                '''                
                from PIL import Image
                im = Image.open(IMAGE_DIR+'/'+bbox_file.replace(".txt", ""))
                im1 = im.crop((int(bbox[1]), int(bbox[2]),int(bbox[3]),int(bbox[4])))
                im1.show()
                '''
                if (bbox[3] > bbox[1]) and (bbox[4] > bbox[2]):
                    ann_writer.writerow([IMAGE_DIR+'/'+bbox_file.replace(".txt", ""), bbox[1], bbox[2],bbox[3],bbox[4],CLASS_NAME])
