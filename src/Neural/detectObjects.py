from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color

import cv2
import os
import numpy as np
import time

from keras_retinanet.models import load_model

#model = load_model('resnet50_coco_best_v2.1.0.h5', backbone_name='resnet50')
model = load_model('gun_model.h5', backbone_name='resnet50')

# load image
image = read_image_bgr('data/weapon/testset/gun8.jpg')

# copy to draw on
draw = image.copy()
draw = cv2.cvtColor(draw, cv2.COLOR_RGB2RGBA)

# preprocess image for network
image = preprocess_image(image)
image, scale = resize_image(image)

# process image
start = time.time()
boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
print("processing time: ", time.time() - start)

# correct for image scale
boxes /= scale

# visualize detections
for box, score, label in zip(boxes[0], scores[0], labels[0]):
    # scores are sorted so we can break
    if score < 0.5:
        break

    color = label_color(label)

    b = box.astype(int)
    draw_box(draw, b, color=color)

    caption = "{} {:.3f}".format(label, score)
    draw_caption(draw, b, caption)

was_written = cv2.imwrite("annotated.jpg", draw)
if was_written:
    print("File written")
else:
    print("File was NOT written")

