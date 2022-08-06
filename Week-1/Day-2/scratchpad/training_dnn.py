# -*- coding: utf-8 -*-
"""Training_DNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mAWGh27QOQULHHqKqaUiz60xtbwD5q3W

tips : pilih toolbar > edit > notebook setting > GPU
"""

import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

data = pd.read_csv('https://raw.githubusercontent.com/fahmimnalfrzki/Dataset/main/kc_house_data.csv').dropna()
data

X = data.drop(columns=['id','date','zipcode'])
y = data['price']

y.mean()

#Memisahkan data menjadi train, val, test

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.9)

X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, train_size=0.8)

len(X.columns)

std = StandardScaler()
X_train_std = std.fit_transform(X_train)
X_val_std = std.transform(X_val)
X_test_std = std.transform(X_test)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(64,input_shape=[len(X.columns)]))
model.add(tf.keras.layers.Dense(32))
model.add(tf.keras.layers.Dense(16))
model.add(tf.keras.layers.Dense(8))
model.add(tf.keras.layers.Dense(1, activation='relu'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.SGD(),
              metrics='mae')

model.summary()

history = model.fit(X_train_std, y_train, epochs=40, batch_size=32,
                    validation_data=(X_val_std, y_val),verbose=1)

"""##Kernel Initializers"""

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(64,input_shape=[len(X.columns)],kernel_initializer=tf.keras.initializers.RandomNormal(seed=40)))
model.add(tf.keras.layers.Dense(32))
model.add(tf.keras.layers.Dense(16))
model.add(tf.keras.layers.Dense(8))
model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.SGD(),
              metrics='mae')

history = model.fit(X_train_std, y_train, epochs=40, batch_size=32,
                    validation_data=(X_val_std, y_val),verbose=1)

"""## Batch Size"""

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(64,input_shape=[len(X.columns)],kernel_initializer=tf.keras.initializers.GlorotNormal(seed=40)))
model.add(tf.keras.layers.Dense(32))
model.add(tf.keras.layers.Dense(16))
model.add(tf.keras.layers.Dense(8))
model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.SGD(),
              metrics='mae')

history = model.fit(X_train_std, y_train, epochs=40, batch_size=70,
                    validation_data=(X_val_std, y_val),verbose=1)

"""## Activation Function"""

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(64,input_shape=[len(X.columns)],kernel_initializer=tf.keras.initializers.GlorotNormal(seed=40)))

model.add(tf.keras.layers.Dense(32,activation='relu'))
model.add(tf.keras.layers.Dense(16,activation='relu'))
model.add(tf.keras.layers.Dense(8,activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.SGD(),
              metrics='mae')

history = model.fit(X_train_std, y_train, epochs=40, batch_size=70,
                    validation_data=(X_val_std, y_val),verbose=1)

fig, ax = plt.subplots()
ax.plot(range(40),history.history['loss'],label='train loss')
ax.plot(range(40),history.history['val_loss'],label='val loss')

ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
plt.legend()

"""##Batch normalization

struktur batch normalization yang sesuai adalah dilakukan sebelum activation function
"""

tf.random.set_seed(42) # gunakan set_seed untuk menghasilkan model yang mempunyai performa yang sama

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(15,input_shape=[len(X.columns)],kernel_initializer=tf.keras.initializers.GlorotNormal(seed=40)))
model.add(tf.keras.layers.Dense(14))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Activation('relu'))

model.add(tf.keras.layers.Dense(10))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Activation('relu'))

model.add(tf.keras.layers.Dense(8))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Activation('relu'))

model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.SGD(),
              metrics='mae')

history = model.fit(X_train_std, y_train, epochs=40, batch_size=70,
                    validation_data=(X_val_std, y_val),verbose=1)

fig, ax = plt.subplots()
ax.plot(range(40),history.history['loss'],label='train loss')
ax.plot(range(40),history.history['val_loss'],label='val loss')
#plt.gca().set_ylim(220000, 223000)
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
plt.legend()

"""## Dropout"""

tf.random.set_seed(42) # gunakan set_seed untuk menghasilkan model yang mempunyai performa yang sama

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(15,input_shape=[len(X.columns)],kernel_initializer=tf.keras.initializers.GlorotNormal(seed=40)))
model.add(tf.keras.layers.Dense(14))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(10))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(8))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.SGD(),
              metrics='mae')

history = model.fit(X_train_std, y_train, epochs=40, batch_size=70,
                    validation_data=(X_val_std, y_val),verbose=1)

fig, ax = plt.subplots()
ax.plot(range(40),history.history['loss'],label='train loss')
ax.plot(range(40),history.history['val_loss'],label='val loss')
#plt.gca().set_ylim(220000, 223000)
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
plt.legend()

"""## Lerning Rate"""

tf.random.set_seed(42) # gunakan set_seed untuk menghasilkan model yang mempunyai performa yang sama

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(15,input_shape=[len(X.columns)],kernel_initializer=tf.keras.initializers.GlorotNormal(seed=40)))
model.add(tf.keras.layers.Dense(14))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(10))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(8))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.SGD(learning_rate=0.0001),
              metrics='mae')

history = model.fit(X_train_std, y_train, epochs=40, batch_size=70,
                    validation_data=(X_val_std, y_val),verbose=1)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(15,input_shape=[len(X.columns)],kernel_initializer=tf.keras.initializers.LecunNormal(seed=40)))
model.add(tf.keras.layers.Dense(14))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(10))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(8))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.SGD(learning_rate=0.08),
              metrics='mae')

history = model.fit(X_train_std, y_train, epochs=40, batch_size=70,
                    validation_data=(X_val_std, y_val),verbose=1)

fig, ax = plt.subplots()
ax.plot(range(40),history.history['loss'],label='train loss')
ax.plot(range(40),history.history['val_loss'],label='val loss')
#plt.gca().set_ylim(220000, 223000)
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
plt.legend()

"""## Gradient Cliping"""

tf.random.set_seed(42) # gunakan set_seed untuk menghasilkan model yang mempunyai performa yang sama

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(15,input_shape=[len(X.columns)],kernel_initializer=tf.keras.initializers.LecunNormal(seed=40)))
model.add(tf.keras.layers.Dense(14))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(10))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(8))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.SGD(clipvalue=1.0),
              metrics='mae')

history = model.fit(X_train_std, y_train, epochs=40, batch_size=70,
                    validation_data=(X_val_std, y_val),verbose=1)

fig, ax = plt.subplots()
ax.plot(range(40),history.history['loss'],label='train loss')
ax.plot(range(40),history.history['val_loss'],label='val loss')
#plt.gca().set_ylim(220000, 223000)
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
plt.legend()

"""## Regularisasi"""

tf.random.set_seed(42) # gunakan set_seed untuk menghasilkan model yang mempunyai performa yang sama

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(15,input_shape=[len(X.columns)],kernel_initializer=tf.keras.initializers.LecunNormal(seed=40)))

model.add(tf.keras.layers.Dense(14,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))

model.add(tf.keras.layers.Dense(10,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))

model.add(tf.keras.layers.Dense(8,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.SGD(learning_rate=0.1),
              metrics='mae')

history = model.fit(X_train_std, y_train, epochs=40, batch_size=70,
                    validation_data=(X_val_std, y_val),verbose=1)

fig, ax = plt.subplots()
ax.plot(range(40),history.history['loss'],label='train loss')
ax.plot(range(40),history.history['val_loss'],label='val loss')
#plt.gca().set_ylim(220000, 223000)
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
plt.legend()

"""## Activation Function Elu"""

tf.random.set_seed(42) # gunakan set_seed untuk menghasilkan model yang mempunyai performa yang sama

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(15,input_shape=[len(X.columns)],kernel_initializer=tf.keras.initializers.LecunNormal(seed=40)))

model.add(tf.keras.layers.Dense(14,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('elu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))

model.add(tf.keras.layers.Dense(10,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('elu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))

model.add(tf.keras.layers.Dense(8,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('elu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.SGD(learning_rate=0.1),
              metrics='mae')

history = model.fit(X_train_std, y_train, epochs=40, batch_size=70,
                    validation_data=(X_val_std, y_val),verbose=1)

fig, ax = plt.subplots()
ax.plot(range(40),history.history['loss'],label='train loss')
ax.plot(range(40),history.history['val_loss'],label='val loss')
#plt.gca().set_ylim(220000, 223000)
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
plt.legend()

"""### Combination Activation Function"""

tf.random.set_seed(42) # gunakan set_seed untuk menghasilkan model yang mempunyai performa yang sama

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(64,input_shape=[len(X.columns)],kernel_initializer=tf.keras.initializers.LecunNormal(seed=40)))

model.add(tf.keras.layers.Dense(60,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('elu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))

model.add(tf.keras.layers.Dense(50,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('selu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))

model.add(tf.keras.layers.Dense(20,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(1, activation='linear'))


model.add(tf.keras.layers.Dense(14,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('elu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))

model.add(tf.keras.layers.Dense(10,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('selu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))

model.add(tf.keras.layers.Dense(8,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('tanh'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.SGD(learning_rate=0.1),
              metrics='mae')

history = model.fit(X_train_std, y_train, epochs=40, batch_size=70,
                    validation_data=(X_val_std, y_val),verbose=1)

fig, ax = plt.subplots()
ax.plot(range(40),history.history['loss'],label='train loss')
ax.plot(range(40),history.history['val_loss'],label='val loss')
#plt.gca().set_ylim(220000, 223000)
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
plt.legend()

"""### Optimaizer"""

tf.random.set_seed(42) # gunakan set_seed untuk menghasilkan model yang mempunyai performa yang sama
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(15,input_shape=[len(X.columns)],kernel_initializer=tf.keras.initializers.LecunNormal(seed=40)))

model.add(tf.keras.layers.Dense(14,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('elu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))

model.add(tf.keras.layers.Dense(10,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('elu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))

model.add(tf.keras.layers.Dense(8,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('elu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.Adam(),
              metrics='mae')

history = model.fit(X_train_std, y_train, epochs=40, batch_size=70,
                    validation_data=(X_val_std, y_val),verbose=1)

fig, ax = plt.subplots()
ax.plot(range(40),history.history['loss'],label='train loss')
ax.plot(range(40),history.history['val_loss'],label='val loss')
#plt.gca().set_ylim(220000, 223000)
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
plt.legend()

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(15,input_shape=[len(X.columns)],kernel_initializer=tf.keras.initializers.LecunNormal(seed=40)))

model.add(tf.keras.layers.Dense(14,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('elu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))

model.add(tf.keras.layers.Dense(10,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('elu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))

model.add(tf.keras.layers.Dense(8,kernel_regularizer=tf.keras.regularizers.l2()))
model.add(tf.keras.layers.Activation('elu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.Nadam(),
              metrics='mae')

history = model.fit(X_train_std, y_train, epochs=40, batch_size=70,
                    validation_data=(X_val_std, y_val),verbose=1)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(64,input_shape=[len(X.columns)],kernel_initializer=tf.keras.initializers.LecunNormal(seed=40)))

model.add(tf.keras.layers.Dense(32))
model.add(tf.keras.layers.Activation('selu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.1))

model.add(tf.keras.layers.Dense(16))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.1))

model.add(tf.keras.layers.Dense(8))
model.add(tf.keras.layers.Activation('elu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.RMSprop(),
              metrics='mae')

history = model.fit(X_train_std, y_train, epochs=40, batch_size=70,
                    validation_data=(X_val_std, y_val),verbose=1)

fig, ax = plt.subplots()
ax.plot(range(40),history.history['loss'],label='train loss')
ax.plot(range(40),history.history['val_loss'],label='val loss')
#plt.gca().set_ylim(220000, 223000)
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
plt.legend()

"""## Momentum & Nesterov"""

tf.random.set_seed(42) # gunakan set_seed untuk menghasilkan model yang mempunyai performa yang sama

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(15,input_shape=[len(X.columns)],kernel_initializer=tf.keras.initializers.GlorotNormal(seed=40)))
model.add(tf.keras.layers.Dense(14))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(10))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(8))
model.add(tf.keras.layers.Activation('relu'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(rate=0.2))
model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.SGD(momentum=0.9, nesterov=True),
              metrics='mae')

history = model.fit(X_train_std, y_train, epochs=40, batch_size=70,
                    validation_data=(X_val_std, y_val),verbose=1)

fig, ax = plt.subplots()
ax.plot(range(40),history.history['loss'],label='train loss')
ax.plot(range(40),history.history['val_loss'],label='val loss')
#plt.gca().set_ylim(220000, 223000)
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
plt.legend()

"""## Final Model"""

tf.random.set_seed(42) # gunakan set_seed untuk menghasilkan model yang mempunyai performa yang sama

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(15,input_shape=[len(X.columns)],kernel_initializer=tf.keras.initializers.GlorotNormal(seed=40)))
model.add(tf.keras.layers.Dense(14))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Activation('relu'))

model.add(tf.keras.layers.Dense(10))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Activation('relu'))

model.add(tf.keras.layers.Dense(8))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Activation('relu'))

model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.SGD(nesterov=True),
              metrics=tf.keras.metrics.RootMeanSquaredError())

history = model.fit(X_train_std, y_train, epochs=40, batch_size=70,
                    validation_data=(X_val_std, y_val),verbose=1)

fig, ax = plt.subplots()
ax.plot(range(40),history.history['loss'],label='train loss')
ax.plot(range(40),history.history['val_loss'],label='val loss')
#plt.gca().set_ylim(220000, 223000)
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
plt.legend()

"""## Evaluation & Prediction"""

model.evaluate(X_test_std, y_test)

X_new = X_test_std[25]

X_new.shape

X_new = X_new.reshape(1,18)

X_new.shape

y_pred = model.predict(X_new)

"""hasil prediksi"""

y_pred

"""membandingkan dengan data asli"""

y_test.iloc[25]

"""## Scaling Y"""

y_train_std = y_train/y_train.max()
y_val_std = y_val/y_val.max()
y_test_std = y_test/y_test.max()

tf.random.set_seed(42) # gunakan set_seed untuk menghasilkan model yang mempunyai performa yang sama

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(15,input_shape=[len(X.columns)],kernel_initializer=tf.keras.initializers.GlorotNormal(seed=40)))
model.add(tf.keras.layers.Dense(14))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Activation('relu'))

model.add(tf.keras.layers.Dense(10))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Activation('relu'))

model.add(tf.keras.layers.Dense(8))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Activation('relu'))

model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss='mae',
              optimizer=tf.keras.optimizers.SGD(nesterov=True),
              metrics=tf.keras.metrics.RootMeanSquaredError())

history = model.fit(X_train_std, y_train_std, epochs=40, batch_size=70,
                    validation_data=(X_val_std, y_val_std),verbose=1)

fig, ax = plt.subplots()
ax.plot(range(40),history.history['loss'],label='train loss')
ax.plot(range(40),history.history['val_loss'],label='val loss')
#plt.gca().set_ylim(220000, 223000)
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
plt.legend()
