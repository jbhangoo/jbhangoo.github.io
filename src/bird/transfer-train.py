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


LEARNING_BIRD_DIR = "data/AZ/"
VALID_PERCENT = 0.2
N_CLASSES = 110
NUMBER_IMAGES = 16434

train_dir = os.path.join(LEARNING_BIRD_DIR, 'train')
test_dir = os.path.join(LEARNING_BIRD_DIR, 'test')

rows = 224
cols= 224

"""# Data Pre-processing"""

base_model = tf.keras.applications.inception_v3.InceptionV3(weights='imagenet', include_top=False, input_shape=(cols,rows,3))

x = base_model.output
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dense(512, activation='relu')(x)
predictions = tf.keras.layers.Dense(N_CLASSES, activation='softmax')(x)

model = tf.keras.Model(inputs=base_model.input, outputs=predictions)

for layer in base_model.layers:
    layer.train = False

model.compile(loss='categorical_crossentropy',
              optimizer=tf.keras.optimizers.RMSprop(lr=1e-4),
              metrics=['acc'])
print (model.summary())

x_train_datagen = ImageDataGenerator(rescale=1./255, horizontal_flip=True, vertical_flip=False, zoom_range=[0.8,1.0],
                                     rotation_range=10, brightness_range=[0.7, 1.1])
train_datagen = x_train_datagen.flow_from_directory(train_dir,
                                                    target_size=(rows,cols),
                                                    batch_size=NUMBER_IMAGES,
                                                    class_mode='categorical')

X, y = train_datagen.next()
print("Training on {} images".format(len(X)))

H = model.fit(X, y, epochs=2, batch_size=32, validation_split=VALID_PERCENT)
model.save("models/birds-az_i3-7.h5")

acc = H.history['acc']
val_acc = H.history['val_acc']
loss = H.history['loss']
val_loss = H.history['val_loss']

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'g', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()
plt.savefig("acc.jpg")

plt.figure()
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'g', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.savefig("loss.jpg")
plt.show()
