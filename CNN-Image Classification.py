
import pandas as pd
import matplotlib.pyplot as plt


from sklearn.model_selection import train_test_split

from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPooling2D, ZeroPadding2D, BatchNormalization, GaussianNoise
from keras.losses import categorical_crossentropy
from keras.callbacks import EarlyStopping
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.datasets import fashion_mnist

((X_train, y_train), (X_test, y_test)) = fashion_mnist.load_data()

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

y_train

print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

"""CROSS Validation"""

X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.10, random_state=42)

print(X_train.shape)
print(X_val.shape)
print(y_train.shape)
print(y_val.shape)

im_rows = 28
im_cols = 28
im_shape = (im_rows, im_cols, 1)

X_train = X_train.reshape(X_train.shape[0], *im_shape)
X_val = X_val.reshape(X_val.shape[0], *im_shape)
X_test = X_test.reshape(X_test.shape[0], *im_shape)

print(X_train.shape)
print(X_val.shape)
print(X_test.shape)

f, ax = plt.subplots(1,5)
f.set_size_inches(80, 40)

for i in range(5):
    ax[i].imshow(X_train[i].reshape(28, 28))
plt.show()

datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.5,
        zoom_range=(0.9, 1.1),
        horizontal_flip=False,
        vertical_flip=False,
        fill_mode='constant',
        cval=0) 


datagen.fit(X_train)

model = Sequential([
    
    Conv2D(32, (3, 3), activation='relu', input_shape=im_shape, padding = 'same'),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    
    Conv2D(64, (3, 3), activation='relu', padding = 'same'),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    
    Conv2D(128, (3, 3), activation='relu', padding = 'same'),
    MaxPooling2D((2, 2)),
    Dropout(0.5),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    
    BatchNormalization(),
    Dense(10, activation='softmax')
])

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)

model.compile(optimizer=Adam(lr=0.001),
             loss='categorical_crossentropy',
             metrics=['accuracy'])

history = model.fit(X_train, y_train,
          batch_size=50, epochs=50, verbose=1, 
          validation_data=(X_val, y_val))

model.summary()

score = model.evaluate(X_test, y_test, verbose=0)
#print(score)

#print('Loss :', score[0])
print('Accuracy : ' + str(score[1] * 100) + '%')

