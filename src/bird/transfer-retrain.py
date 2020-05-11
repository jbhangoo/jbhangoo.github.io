'''
Pipeline Source:
https://colab.research.google.com/drive/1kcRinhBB3M6vuZJmOEssQZo5wjRMgEVF

Data Source:
https://www.kaggle.com/gpiosenka/100-bird-species

References:

1. [Anthony Tanbakuchi](http://tanbakuchi.com/posts/comparison-of-openv-interpolation-algorithms/ )
'''

import tensorflow as tf
import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from tensorflow.keras.models import load_model

LEARNING_BIRD_DIR = "data/AZ/"

train_dir = os.path.join(LEARNING_BIRD_DIR, 'train')
test_dir = os.path.join(LEARNING_BIRD_DIR, 'test')

rows = 224
cols= 224

model = load_model("../ML-course/models/birds-az_i3-2.h5")
print (model.summary())

x_train_datagen = ImageDataGenerator(rescale=1./255, horizontal_flip=True, vertical_flip=False, zoom_range=0.2,
                                     rotation_range=10, brightness_range=[0.7, 1.0])

train_datagen = x_train_datagen.flow_from_directory(LEARNING_BIRD_DIR+"/train",
                                                    target_size=(rows,cols),
                                                    batch_size=17219,
                                                    class_mode='categorical')

X, y = train_datagen.next()
print("Re-Training on {} images".format(len(X)))

H = model.fit(X, y, epochs=1, batch_size=32, validation_split=0.2)
model.save("models/birds-az_i3-3.h5")

acc = H.history['acc']
val_acc = H.history['val_acc']
loss = H.history['loss']
val_loss = H.history['val_loss']

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'g', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()
plt.savefig("acc-az2.jpg")

plt.figure()
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'g', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.savefig("loss-az2.jpg")
plt.show()
