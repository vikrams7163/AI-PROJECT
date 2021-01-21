# -*- coding: utf-8 -*-
"""Notes Classification_final_30

Automatically generated by Colaboratory.
	    @script-author: Srija Srinivasan, Vikram Shakthi, Rakshith RP
	    @script-description: Python code to build classification models to predict real and fake Indian currency   
    	@script-details: Written in Google Colaboratory

Original file is located at
    https://colab.research.google.com/drive/1EEl894ayiyvz7zGGR58fyLE6ZPC3QWPp
"""

from google.colab import drive
drive.mount('/content/drive')

from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator,load_img
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Conv2D

import numpy as np
from glob import glob

train_dir='/content/drive/MyDrive/Jackpot/outputimg/train'
test_dir='/content/drive/MyDrive/Jackpot/outputimg/val'

img_width, img_height= 224,224

Classifier=Sequential()

Classifier.add(Conv2D(32,(3,3), input_shape=(224,224,1), activation='relu'))
Classifier.add(MaxPooling2D(pool_size=(2,2)))

Classifier.add(Conv2D(32,(3,3),activation='relu'))
Classifier.add(MaxPooling2D(pool_size=(2,2)))

Classifier.add(Flatten())

Classifier.add(Dense(units = 128, activation = 'relu'))
Classifier.add(Dense(units = 10, activation = 'softmax'))
Classifier.summary()

Classifier.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)

from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   height_shift_range=0.2,
                                   featurewise_center=True,
                                   rotation_range=0.4,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255,)

training_set = train_datagen.flow_from_directory(train_dir,
                                                 target_size = (224, 224),
                                                 batch_size = 32,
                                                 color_mode ='grayscale',
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory(test_dir,
                                            target_size = (224, 224),
                                            batch_size = 32,
                                            color_mode='grayscale',
                                            class_mode = 'categorical')

from PIL import _imaging
from PIL import Image
import PIL
# Run the cell. It will take some time to execute
r = Classifier.fit_generator(
  training_set,
  validation_data=test_set,
  epochs=30,
  steps_per_epoch=len(training_set),
  validation_steps=len(test_set)
)

r.history

import matplotlib.pyplot as plt
# plot the loss
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.show()
plt.savefig('LossVal_loss')

# plot the accuracy
plt.plot(r.history['accuracy'], label='train acc')
plt.plot(r.history['val_accuracy'], label='val acc')
plt.legend()
plt.show()
plt.savefig('AccVal_acc')

from tensorflow.keras.models import load_model

Classifier.save('model_Classifierf.h5')

y_pred = Classifier.predict(test_set)

y_pred

import numpy as np
y_pred = np.argmax(y_pred, axis=1)

y_pred



from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

model=load_model('model_Classifierf.h5')

img=image.load_img('/content/drive/MyDrive/BDA/50(10).jpg',target_size=(224,224),color_mode='grayscale')

img

test_image=image.img_to_array(img)
test_image=np.expand_dims(test_image, axis = 0)

result = Classifier.predict(test_image)
result

a=np.argmax(model.predict(test_image), axis=1)

for i in a:
  print(i)

model.evaluate(test_set)

model.evaluate(training_set)

