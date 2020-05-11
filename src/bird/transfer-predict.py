import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from sklearn.metrics import precision_score, recall_score, f1_score
LEARNING_BIRD_DIR = "data/AZ/"

train_dir = os.path.join(LEARNING_BIRD_DIR, 'train')
test_dir = os.path.join(LEARNING_BIRD_DIR, 'test')

rows = 224
cols= 224

def load_image(img_path):

    img = image.load_img(img_path, target_size=(cols, rows))
    img_tensor = image.img_to_array(img)                    # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.                                      # imshow expects values in the range [0, 1]
    return img_tensor

# Get class names from all the folders the model was trained on
class_names = os.listdir(train_dir)
class_names = sorted(class_names)
n_classes = len(class_names)
class_labels = dict(zip(range(n_classes), class_names))
print (class_labels)

# The species label for each image in the test subdirectory is the directory name
model = load_model("models/birds-az_i3-7.h5")
test_dirs = os.listdir(test_dir)

# Build a confusion matrix of testing results
confusion = np.zeros((n_classes, n_classes))
y_pred = []
y_act = []
i = 0
for i in range(n_classes):
    species = test_dirs[i]
    imgs = os.listdir(os.path.join(test_dir, species))
    for img in imgs:
        img_path = test_dir + '/' + species + '/' + img
        new_image = load_image(img_path)
        pred = model.predict(new_image)
        pred_idx = np.argmax(pred)
        y_pred.append(pred_idx)
        y_act.append(i)

prec = precision_score(y_act, y_pred, average='macro')
rec = recall_score(y_act, y_pred, average='macro')
f1 = f1_score(y_act, y_pred, average='macro')
print('PREC\tREC\tF1')
print('{}\t{}\t{}'.format(round(prec, 3), round(rec, 3), round(f1, 3)))

print("DONE")
