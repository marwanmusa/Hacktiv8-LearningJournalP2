# -*- coding: utf-8 -*-
"""
Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k81LsJ3ODEXEkFaQsqqOBN4s6xdbhYmU

# Artificial Neural Network Landscape with Keras

Today afternoon session, we will learn about:
- Using NN for Classification
- Using NN for Regression

# Setup

First, let's import a few common modules, ensure MatplotLib plots figures inline and prepare a function to save the figures. We also check that Python 3.5 or later is installed (although Python 2.x may work, it is deprecated so we strongly recommend you use Python 3 instead), as well as Scikit-Learn ≥0.20 and TensorFlow ≥2.0.
"""

!nvidia-smi

# Commented out IPython magic to ensure Python compatibility.
# Python ≥3.5 is required
import sys

# Scikit-Learn ≥0.20 is required
import sklearn

# TensorFlow ≥2.0 is required
import tensorflow as tf

# Common imports
import numpy as np
import os

# to make this notebook's output stable across runs
np.random.seed(42)

# To plot pretty figures
# %matplotlib inline
import matplotlib as mpl

from tensorflow import keras

"""# Building an Image Classifier

First let's import TensorFlow and Keras.
"""

import tensorflow as tf
from tensorflow import keras

tf.__version__

keras.__version__

"""The second version is the version of the Keras API implemented by tf.keras. Note that
it ends with -tf, highlighting the fact that tf.keras implements the Keras API, plus
some extra TensorFlow-specific features.

Now let’s use tf.keras! We’ll start by building a simple image classifier.

## Building an Image Classifier Using the Sequential API

First, we need to load a dataset. In this chapter we will tackle Fashion MNIST, which
is a drop-in replacement of MNIST. It has the exact same
format as MNIST (70,000 grayscale images of 28 × 28 pixels each, with 10 classes),
but the images represent fashion items rather than handwritten digits, so each class is
more diverse, and the problem turns out to be significantly more challenging than
MNIST. For example, a simple linear model reaches about 92% accuracy on MNIST,
but only about 83% on Fashion MNIST.

Let's start by loading the fashion MNIST dataset. Keras has a number of functions to load popular datasets in `keras.datasets`. The dataset is already split for you between a training set and a test set, but it can be useful to split the training set further to have a validation set:
"""

fashion_mnist = keras.datasets.fashion_mnist
(X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()

"""When loading MNIST or Fashion MNIST using Keras rather than Scikit-Learn, one
important difference is that every image is represented as a 28 × 28 array rather than
a 1D array of size 784. Moreover, the pixel intensities are represented as integers
(from 0 to 255) rather than floats (from 0.0 to 255.0). Let’s take a look at the shape
and data type of the training set:
"""

X_train_full.shape

"""Each pixel intensity is represented as a byte (0 to 255):"""

X_train_full.dtype

"""Note that the dataset is already split into a training set and a test set, but there is no
validation set, so we’ll create one now. Additionally, since we are going to train the
neural network using Gradient Descent, we must scale the input features. For simplic‐
ity, we’ll scale the pixel intensities down to the 0–1 range by dividing them by 255.0
(this also converts them to floats):
"""

X_valid, X_train = X_train_full[:5000] / 255., X_train_full[5000:] / 255.
y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
X_test = X_test / 255.

"""You can plot an image using Matplotlib's `imshow()` function, with a `'binary'`
 color map:
"""

plt.imshow(X_train[0], cmap="binary")
plt.axis('off')
plt.show()

"""The labels are the class IDs (represented as uint8), from 0 to 9:"""

y_train

"""Here are the corresponding class names:"""

class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
               "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

"""So the first image in the training set is a coat:"""

class_names[y_train[0]]

"""The validation set contains 5,000 images, and the test set contains 10,000 images:"""

X_valid.shape

X_test.shape

"""Let's take a look at a sample of the images in the dataset:"""

n_rows = 4
n_cols = 10
plt.figure(figsize=(n_cols * 1.2, n_rows * 1.2))
for row in range(n_rows):
    for col in range(n_cols):
        index = n_cols * row + col
        plt.subplot(n_rows, n_cols, index + 1)
        plt.imshow(X_train[index], cmap="binary", interpolation="nearest")
        plt.axis('off')
        plt.title(class_names[y_train[index]], fontsize=12)
plt.subplots_adjust(wspace=0.2, hspace=0.5)
save_fig('fashion_mnist_plot', tight_layout=False)
plt.show()

"""## Creating the model using the Sequential API

Now let’s build the neural network! Here is a classification MLP with two hidden
layers:
"""

model = keras.models.Sequential()
model.add(keras.layers.Flatten(input_shape=[28, 28]))
model.add(keras.layers.Dense(300, activation="relu"))
model.add(keras.layers.Dense(100, activation="relu"))
model.add(keras.layers.Dense(10, activation="softmax"))

"""Let’s go through this code line by line:

- The first line creates a Sequential model. This is the simplest kind of Keras
model for neural networks that are just composed of a single stack of layers connected sequentially. This is called the Sequential API.
- Next, we build the first layer and add it to the model. It is a Flatten layer whose
role is to convert each input image into a 1D array: if it receives input data X, it
computes X.reshape(-1, 1). This layer does not have any parameters; it is just
there to do some simple preprocessing. Since it is the first layer in the model, you
should specify the input_shape, which doesn’t include the batch size, only the
shape of the instances. Alternatively, you could add a keras.layers.InputLayer
as the first layer, setting input_shape=[28,28].
- Next we add a Dense hidden layer with 300 neurons. It will use the ReLU activation function. Each Dense layer manages its own weight matrix, containing all the
connection weights between the neurons and their inputs. It also manages a vector of bias terms (one per neuron).
- Then we add a second Dense hidden layer with 100 neurons, also using the ReLU
activation function.
- Finally, we add a Dense output layer with 10 neurons (one per class), using the
softmax activation function (because the classes are exclusive).
"""

keras.backend.clear_session()
np.random.seed(42)
tf.random.set_seed(42)

"""Instead of adding the layers one by one as we just did, you can pass a list of layers
when creating the Sequential model:
"""

model = keras.models.Sequential([
    keras.layers.Flatten(input_shape=[28, 28]),
    keras.layers.Dense(300, activation="relu"),
    keras.layers.Dense(100, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
])

model.layers

"""The model’s summary() method displays all the model’s layers, including each layer’s
name (which is automatically generated unless you set it when creating the layer), its
output shape (None means the batch size can be anything), and its number of parameters. The summary ends with the total number of parameters, including trainable and
non-trainable parameters. Here we only have trainable parameters.
"""

model.summary()

"""- 100x300+100= 30100
- 100x10+100= 1010

Note that Dense layers often have a lot of parameters. For example, the first hidden
layer has 784 × 300 connection weights, plus 300 bias terms, which adds up to
235,500 parameters! This gives the model quite a lot of flexibility to fit the training
data, but it also means that the model runs the risk of overfitting, especially when you
do not have a lot of training data.
"""

keras.utils.plot_model(model, "my_fashion_mnist_model.png", show_shapes=True)

hidden1 = model.layers[1]
hidden1.name

model.get_layer(hidden1.name) is hidden1

weights, biases = hidden1.get_weights()

weights

weights.shape

biases

biases.shape

"""## Compiling the model

After a model is created, you must call its compile() method to specify the loss function and the optimizer to use. Optionally, you can specify a list of extra metrics to
compute during training and evaluation:
"""

model.compile(loss="sparse_categorical_crossentropy",
              optimizer="sgd",
              metrics=["accuracy"])

"""This is equivalent to:

```python
model.compile(loss=keras.losses.sparse_categorical_crossentropy,
              optimizer=keras.optimizers.SGD(),
              metrics=[keras.metrics.sparse_categorical_accuracy])
```

This code requires some explanation. First, we use the "sparse_categorical_cross
entropy" loss because we have sparse labels (i.e., for each instance, there is just a target class index, from 0 to 9 in this case), and the classes are exclusive. If instead we
had one target probability per class for each instance (such as one-hot vectors, e.g.
`[0., 0., 0., 1., 0., 0., 0., 0., 0., 0.]` to represent class 3), then we would
need to use the "categorical_crossentropy" loss instead. If we were doing binary
classification (with one or more binary labels), then we would use the "sigmoid" (i.e.,
logistic) activation function in the output layer instead of the "softmax" activation
function, and we would use the "binary_crossentropy" loss.

Regarding the optimizer, "sgd" means that we will train the model using simple Stochastic Gradient Descent. In other words, Keras will perform the backpropagation
algorithm described earlier (i.e., reverse-mode autodiff plus Gradient Descent).

Finally, since this is a classifier, it’s useful to measure its "accuracy" during training
and evaluation.

## Training and evaluating the model

Now the model is ready to be trained. For this we simply need to call its fit()
method:
"""

history = model.fit(X_train, y_train, epochs=30,
                    validation_data=(X_valid, y_valid))

"""We pass it the input features (X_train) and the target classes (y_train), as well as the
number of epochs to train (or else it would default to just 1, which would definitely
not be enough to converge to a good solution). We also pass a validation set (this is
optional). Keras will measure the loss and the extra metrics on this set at the end of
each epoch, which is very useful to see how well the model really performs. If the performance on the training set is much better than on the validation set, your model is probably overfitting the training set (or there is a bug, such as a data mismatch
between the training set and the validation set).

And that’s it! The neural network is trained. At each epoch during training, Keras
displays the number of instances processed so far (along with a progress bar), the
mean training time per sample, and the loss and accuracy (or any other extra metrics
you asked for) on both the training set and the validation set. You can see that the
training loss went down, which is a good sign, and the validation accuracy reached
89.26% after 30 epochs. That’s not too far from the training accuracy, so there does
not seem to be much overfitting going on.

If the training set was very skewed, with some classes being overrepresented and others underrepresented, it would be useful to set the class_weight argument when
calling the fit() method, which would give a larger weight to underrepresented
classes and a lower weight to overrepresented classes. These weights would be used by
Keras when computing the loss. If you need per-instance weights, set the sam
ple_weight argument (if both class_weight and sample_weight are provided, Keras
multiplies them). Per-instance weights could be useful if some instances were labeled
by experts while others were labeled using a crowdsourcing platform: you might want
to give more weight to the former. You can also provide sample weights (but not class
weights) for the validation set by adding them as a third item in the validation_data
tuple.
"""

history.params

"""The fit() method returns a History object containing the training parameters
(history.params), the list of epochs it went through (history.epoch), and most
importantly a dictionary (history.history) containing the loss and extra metrics it
measured at the end of each epoch on the training set and on the validation set (if
any). If you use this dictionary to create a pandas DataFrame and call its plot()
method,
"""

print(history.epoch)

history.history.keys()

import pandas as pd

pd.DataFrame(history.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1)
save_fig("keras_learning_curves_plot")
plt.show()

"""You can see that both the training accuracy and the validation accuracy steadily
increase during training, while the training loss and the validation loss decrease.
Good! Moreover, the validation curves are close to the training curves, which means
that there is not too much overfitting. In this particular case, the model looks like it
performed better on the validation set than on the training set at the beginning of
training. But that’s not the case: indeed, the validation error is computed at the end of
each epoch, while the training error is computed using a running mean during each
epoch. So the training curve should be shifted by half an epoch to the left. If you do
that, you will see that the training and validation curves overlap almost perfectly at
the beginning of training.

The training set performance ends up beating the validation performance, as is gen‐
erally the case when you train for long enough. You can tell that the model has not
quite converged yet, as the validation loss is still going down, so you should probably
continue training. It’s as simple as calling the fit() method again, since Keras just
continues training where it left off (you should be able to reach close to 89% validation accuracy).
If you are not satisfied with the performance of your model, you should go back and
tune the hyperparameters. The first one to check is the learning rate. If that doesn’t
help, try another optimizer (and always retune the learning rate after changing any
hyperparameter). If the performance is still not great, then try tuning model hyperparameters such as the number of layers, the number of neurons per layer, and the
types of activation functions to use for each hidden layer. You can also try tuning
other hyperparameters, such as the batch size (it can be set in the fit() method using
the batch_size argument, which defaults to 32). We will get back to hyperparameter
tuning at the end of this chapter. Once you are satisfied with your model’s validation
accuracy, you should evaluate it on the test set to estimate the generalization error
before you deploy the model to production. You can easily do this using the evalu
ate() method (it also supports several other arguments, such as batch_size and
sample_weight; please check the documentation for more details):
"""

model.evaluate(X_test, y_test)

"""it is common to get slightly lower performance on the test set
than on the validation set, because the hyperparameters are tuned on the validation
set, not the test set (however, in this example, we did not do any hyperparameter tun‐
ing, so the lower accuracy is just bad luck). Remember to resist the temptation to
tweak the hyperparameters on the test set, or else your estimate of the generalization
error will be too optimistic.

## Using the model to make predictions

Next, we can use the model’s predict() method to make predictions on new instan‐
ces. Since we don’t have actual new instances, we will just use the first three instances
of the test set:
"""

X_new = X_test[:3]
y_proba = model.predict(X_new)
y_proba.round(2)

"""As you can see, for each instance the model estimates one probability per class, from
class 0 to class 9. For example, for the first image it estimates that the probability of
class 9 (ankle boot) is 96%, the probability of class 5 (sandal) is 3%, the probability of
class 7 (sneaker) is 1%, and the probabilities of the other classes are negligible. In
other words, it “believes” the first image is footwear, most likely ankle boots but possibly sandals or sneakers. If you only care about the class with the highest estimated
probability (even if that probability is quite low), then you can use the pre
dict_classes() method instead:

**Warning**: `model.predict_classes(X_new)` is deprecated. It is replaced with `np.argmax(model.predict(X_new), axis=-1)`.
"""

#y_pred = model.predict_classes(X_new) # deprecated
y_pred = np.argmax(model.predict(X_new), axis=-1)
y_pred

np.array(class_names)[y_pred]

"""Here, the classifier actually classified all three images correctly."""

y_new = y_test[:3]
y_new

plt.figure(figsize=(7.2, 2.4))
for index, image in enumerate(X_new):
    plt.subplot(1, 3, index + 1)
    plt.imshow(image, cmap="binary", interpolation="nearest")
    plt.axis('off')
    plt.title(class_names[y_test[index]], fontsize=12)
plt.subplots_adjust(wspace=0.2, hspace=0.5)
save_fig('fashion_mnist_images_plot', tight_layout=False)
plt.show()

"""# Regression MLP

Let’s switch to the California housing problem and tackle it using a regression neural
network. For simplicity, we will use Scikit-Learn’s fetch_california_housing()
function to load the data. After loading the data, we split it into a training set, a vali‐
dation set, and a test set, and we scale all the features:
"""

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
import tensorflow as tf
from tensorflow import keras

housing = fetch_california_housing()

X_train_full, X_test, y_train_full, y_test = train_test_split(housing.data, housing.target, random_state=42)
X_train, X_valid, y_train, y_valid = train_test_split(X_train_full, y_train_full, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_valid = scaler.transform(X_valid)
X_test = scaler.transform(X_test)

print(housing['DESCR'])

x_cuy= housing.data
y_cuy= housing.target

df= pd.DataFrame(x_cuy,columns= housing.feature_names)
df

np.random.seed(42)
tf.random.set_seed(42)

"""Using the Sequential API to build, train, evaluate, and use a regression MLP to make
predictions is quite similar to what we did for classification. The main differences are
the fact that the output layer has a single neuron (since we only want to predict a single value) and uses no activation function, and the loss function is the mean squared
error. Since the dataset is quite noisy, we just use a single hidden layer with fewer
neurons than before, to avoid overfitting:
"""

model = keras.models.Sequential([
    keras.layers.Dense(30, activation="relu", input_shape=X_train.shape[1:]),
    keras.layers.Dense(1)
])
model.compile(loss="mean_squared_error", optimizer=keras.optimizers.SGD(lr=1e-3))
history = model.fit(X_train, y_train, epochs=20, validation_data=(X_valid, y_valid))
mse_test = model.evaluate(X_test, y_test)
X_new = X_test[:3]
y_pred = model.predict(X_new)

"""As you can see, the Sequential API is quite easy to use. However, although Sequen
tial models are extremely common, it is sometimes useful to build neural networks
with more complex topologies, or with multiple inputs or outputs. For this purpose,
Keras offers the Functional API.
"""

plt.plot(pd.DataFrame(history.history))
plt.grid(True)
plt.gca().set_ylim(0, 1)
plt.show()

y_pred

"""# Functional API

Not all neural network models are simply sequential. Some may have complex topologies. Some may have multiple inputs and/or multiple outputs. For example, a Wide & Deep neural network (see [paper](https://ai.google/research/pubs/pub45413)) connects all or part of the inputs directly to the output layer.
"""

np.random.seed(42)
tf.random.set_seed(42)

"""Let’s build such a neural network to tackle the California housing problem:"""

input_ = keras.layers.Input(shape=X_train.shape[1:])
hidden1 = keras.layers.Dense(30, activation="relu")(input_)
hidden2 = keras.layers.Dense(30, activation="relu")(hidden1)
concat = keras.layers.concatenate([input_, hidden2])
output = keras.layers.Dense(1)(concat)
model = keras.models.Model(inputs=[input_], outputs=[output])

"""Let’s go through each line of this code:

- First, we need to create an Input object.18 This is a specification of the kind of
input the model will get, including its shape and dtype. A model may actually
have multiple inputs, as we will see shortly.
- Next, we create a Dense layer with 30 neurons, using the ReLU activation func‐
tion. As soon as it is created, notice that we call it like a function, passing it the
input. This is why this is called the Functional API. Note that we are just telling
Keras how it should connect the layers together; no actual data is being processed
yet.
- We then create a second hidden layer, and again we use it as a function. Note that
we pass it the output of the first hidden layer.
- Next, we create a Concatenate layer, and once again we immediately use it like a
function, to concatenate the input and the output of the second hidden layer. You
may prefer the keras.layers.concatenate() function, which creates a
Concatenate layer and immediately calls it with the given inputs.
- Then we create the output layer, with a single neuron and no activation function,
and we call it like a function, passing it the result of the concatenation.
- Lastly, we create a Keras Model, specifying which inputs and outputs to use.

Once you have built the Keras model, everything is exactly like earlier, so there’s no
need to repeat it here: you must compile the model, train it, evaluate it, and use it to
make predictions.
"""

model.summary()

model.compile(loss="mean_squared_error", optimizer=keras.optimizers.SGD(lr=1e-3))
history = model.fit(X_train, y_train, epochs=20,
                    validation_data=(X_valid, y_valid))
mse_test = model.evaluate(X_test, y_test)
y_pred = model.predict(X_new)

"""But what if you want to send a subset of the features through the wide path and a
different subset (possibly overlapping) through the deep path? In
this case, one solution is to use multiple inputs. For example, suppose we want to
send five features through the wide path (features 0 to 4), and six features through the
deep path (features 2 to 7):
"""

np.random.seed(42)
tf.random.set_seed(42)

input_A = keras.layers.Input(shape=[5], name="wide_input")
input_B = keras.layers.Input(shape=[6], name="deep_input")
hidden1 = keras.layers.Dense(30, activation="relu")(input_B)
hidden2 = keras.layers.Dense(30, activation="relu")(hidden1)
concat = keras.layers.concatenate([input_A, hidden2])
output = keras.layers.Dense(1, name="output")(concat)
model = keras.models.Model(inputs=[input_A, input_B], outputs=[output])

"""The code is self-explanatory. You should name at least the most important layers,
especially when the model gets a bit complex like this. Note that we specified
`inputs=[input_A, input_B]` when creating the model. Now we can compile the
model as usual, but when we call the fit() method, instead of passing a single input
matrix X_train, we must pass a pair of matrices (X_train_A, X_train_B): one per
input. The same is true for X_valid, and also for X_test and X_new when you call
evaluate() or predict():
"""

model.compile(loss="mse", optimizer=keras.optimizers.SGD(lr=1e-3))

X_train_A, X_train_B = X_train[:, :5], X_train[:, 2:]
X_valid_A, X_valid_B = X_valid[:, :5], X_valid[:, 2:]
X_test_A, X_test_B = X_test[:, :5], X_test[:, 2:]
X_new_A, X_new_B = X_test_A[:3], X_test_B[:3]

history = model.fit((X_train_A, X_train_B), y_train, epochs=20,
                    validation_data=((X_valid_A, X_valid_B), y_valid))
mse_test = model.evaluate((X_test_A, X_test_B), y_test)
y_pred = model.predict((X_new_A, X_new_B))

"""There are many use cases in which you may want to have multiple outputs:

- The task may demand it. For instance, you may want to locate and classify the
main object in a picture. This is both a regression task (finding the coordinates of
the object’s center, as well as its width and height) and a classification task.
- Similarly, you may have multiple independent tasks based on the same data. Sure,
you could train one neural network per task, but in many cases you will get better
results on all tasks by training a single neural network with one output per task.
This is because the neural network can learn features in the data that are useful
across tasks. For example, you could perform multitask classification on pictures
of faces, using one output to classify the person’s facial expression (smiling, surprised, etc.) and another output to identify whether they are wearing glasses or
not.
- Another use case is as a regularization technique (i.e., a training constraint whose
objective is to reduce overfitting and thus improve the model’s ability to generalize). For example, you may want to add some auxiliary outputs in a neural network architecture to ensure that the underlying part of the
network learns something useful on its own, without relying on the rest of the
network.

Adding extra outputs is quite easy: just connect them to the appropriate layers and
add them to your model’s list of outputs.
"""

np.random.seed(42)
tf.random.set_seed(42)

input_A = keras.layers.Input(shape=[5], name="wide_input")
input_B = keras.layers.Input(shape=[6], name="deep_input")
hidden1 = keras.layers.Dense(30, activation="relu")(input_B)
hidden2 = keras.layers.Dense(30, activation="relu")(hidden1)
concat = keras.layers.concatenate([input_A, hidden2])
output = keras.layers.Dense(1, name="main_output")(concat)
aux_output = keras.layers.Dense(1, name="aux_output")(hidden2)
model = keras.models.Model(inputs=[input_A, input_B],
                           outputs=[output, aux_output])

"""Each output will need its own loss function. Therefore, when we compile the model,
we should pass a list of losses20 (if we pass a single loss, Keras will assume that the
same loss must be used for all outputs). By default, Keras will compute all these losses
and simply add them up to get the final loss used for training. We care much more
about the main output than about the auxiliary output (as it is just used for regularization), so we want to give the main output’s loss a much greater weight. Fortunately,
it is possible to set all the loss weights when compiling the model:
"""

model.compile(loss=["mse", "mse"], loss_weights=[0.9, 0.1], optimizer=keras.optimizers.SGD(lr=1e-3))

"""Now when we train the model, we need to provide labels for each output. In this
example, the main output and the auxiliary output should try to predict the same
thing, so they should use the same labels. So instead of passing y_train, we need to
pass (y_train, y_train) (and the same goes for y_valid and y_test):
"""

history = model.fit([X_train_A, X_train_B], [y_train, y_train], epochs=20,
                    validation_data=([X_valid_A, X_valid_B], [y_valid, y_valid]))

"""When we evaluate the model, Keras will return the total loss, as well as all the individual losses:"""

total_loss, main_loss, aux_loss = model.evaluate(
    [X_test_A, X_test_B], [y_test, y_test])
y_pred_main, y_pred_aux = model.predict([X_new_A, X_new_B])

"""# The subclassing API

Both the Sequential API and the Functional API are declarative: you start by declaring which layers you want to use and how they should be connected, and only then
can you start feeding the model some data for training or inference. This has many
advantages: the model can easily be saved, cloned, and shared; its structure can be
displayed and analyzed; the framework can infer shapes and check types, so errors
can be caught early (i.e., before any data ever goes through the model). It’s also fairly
easy to debug, since the whole model is a static graph of layers. But the flip side is just
that: it’s static. Some models involve loops, varying shapes, conditional branching,
and other dynamic behaviors. For such cases, or simply if you prefer a more imperative programming style, the Subclassing API is for you.

Simply subclass the Model class, create the layers you need in the constructor, and use
them to perform the computations you want in the call() method. For example, creating an instance of the following WideAndDeepModel class gives us an equivalent
model to the one we just built with the Functional API. You can then compile it, evaluate it, and use it to make predictions, exactly like we just did:
"""

class WideAndDeepModel(keras.models.Model):
    def __init__(self, units=30, activation="relu", **kwargs):
        super().__init__(**kwargs)
        self.hidden1 = keras.layers.Dense(units, activation=activation)
        self.hidden2 = keras.layers.Dense(units, activation=activation)
        self.main_output = keras.layers.Dense(1)
        self.aux_output = keras.layers.Dense(1)
        
    def call(self, inputs):
        input_A, input_B = inputs
        hidden1 = self.hidden1(input_B)
        hidden2 = self.hidden2(hidden1)
        concat = keras.layers.concatenate([input_A, hidden2])
        main_output = self.main_output(concat)
        aux_output = self.aux_output(hidden2)
        return main_output, aux_output

model = WideAndDeepModel(30, activation="relu")

model.compile(loss="mse", loss_weights=[0.9, 0.1], optimizer=keras.optimizers.SGD(lr=1e-3))
history = model.fit((X_train_A, X_train_B), (y_train, y_train), epochs=10,
                    validation_data=((X_valid_A, X_valid_B), (y_valid, y_valid)))
total_loss, main_loss, aux_loss = model.evaluate((X_test_A, X_test_B), (y_test, y_test))
y_pred_main, y_pred_aux = model.predict((X_new_A, X_new_B))

"""This example looks very much like the Functional API, except we do not need to create the inputs; we just use the input argument to the call() method, and we separate
the creation of the layers21 in the constructor from their usage in the call() method.
The big difference is that you can do pretty much anything you want in the call()
method: for loops, if statements, low-leveTensorFlow operations—your imagination is the limit! This makes it a great API for researchers experi‐
menting with new ideas.

This extra flexibility does come at a cost: your model’s architecture is hidden within
the call() method, so Keras cannot easily inspect it; it cannot save or clone it; and
when you call the summary() method, you only get a list of layers, without any information on how they are connected to each other. Moreover, Keras cannot check types
and shapes ahead of time, and it is easier to make mistakes. So unless you really need
that extra flexibility, you should probably stick to the Sequential API or the Functional API.

# Saving and Restoring
"""

np.random.seed(42)
tf.random.set_seed(42)

model = keras.models.Sequential([
    keras.layers.Dense(30, activation="relu", input_shape=[8]),
    keras.layers.Dense(30, activation="relu"),
    keras.layers.Dense(1)
])

model.compile(loss="mse", optimizer=keras.optimizers.SGD(lr=1e-3))
history = model.fit(X_train, y_train, epochs=10, validation_data=(X_valid, y_valid))
mse_test = model.evaluate(X_test, y_test)

model.save("my_keras_model.h5")

"""Keras will use the HDF5 format to save both the model’s architecture (including every
layer’s hyperparameters) and the values of all the model parameters for every layer
(e.g., connection weights and biases). It also saves the optimizer (including its hyperparameters and any state it may have).

You will typically have a script that trains a model and saves it, and one or more
scripts (or web services) that load the model and use it to make predictions. Loading
the model is just as easy:
"""

model = keras.models.load_model("my_keras_model.h5")

model.predict(X_new)

model.save_weights("my_keras_weights.ckpt")

model.load_weights("my_keras_weights.ckpt")

"""But what if training lasts several hours? This is quite common, especially when training on large datasets. In this case, you should not only save your model at the end of
training, but also save checkpoints at regular intervals during training, to avoid losing
everything if your computer crashes. But how can you tell the fit() method to save
checkpoints? Use callbacks.

# Using Callbacks during Training
"""

keras.backend.clear_session()
np.random.seed(42)
tf.random.set_seed(42)

model = keras.models.Sequential([
    keras.layers.Dense(30, activation="relu", input_shape=[8]),
    keras.layers.Dense(30, activation="relu"),
    keras.layers.Dense(1)
])

model.compile(loss="mse", optimizer=keras.optimizers.SGD(lr=1e-3))
checkpoint_cb = keras.callbacks.ModelCheckpoint("my_keras_model.h5", save_best_only=True)
history = model.fit(X_train, y_train, epochs=10,
                    validation_data=(X_valid, y_valid),
                    callbacks=[checkpoint_cb])
model = keras.models.load_model("my_keras_model.h5") # rollback to best model
mse_test = model.evaluate(X_test, y_test)

model.compile(loss="mse", optimizer=keras.optimizers.SGD(lr=1e-3))
early_stopping_cb = keras.callbacks.EarlyStopping(patience=10,
                                                  restore_best_weights=True)
history = model.fit(X_train, y_train, epochs=100,
                    validation_data=(X_valid, y_valid),
                    callbacks=[checkpoint_cb, early_stopping_cb])
mse_test = model.evaluate(X_test, y_test)

class PrintValTrainRatioCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        print("\nval/train: {:.2f}".format(logs["val_loss"] / logs["loss"]))

val_train_ratio_cb = PrintValTrainRatioCallback()
history = model.fit(X_train, y_train, epochs=1,
                    validation_data=(X_valid, y_valid),
                    callbacks=[val_train_ratio_cb])

"""# TensorBoard"""

root_logdir = os.path.join(os.curdir, "my_logs")

def get_run_logdir():
    import time
    run_id = time.strftime("run_%Y_%m_%d-%H_%M_%S")
    return os.path.join(root_logdir, run_id)

run_logdir = get_run_logdir()
run_logdir

keras.backend.clear_session()
np.random.seed(42)
tf.random.set_seed(42)

model = keras.models.Sequential([
    keras.layers.Dense(30, activation="relu", input_shape=[8]),
    keras.layers.Dense(30, activation="relu"),
    keras.layers.Dense(1)
])    
model.compile(loss="mse", optimizer=keras.optimizers.SGD(lr=1e-3))

tensorboard_cb = keras.callbacks.TensorBoard(run_logdir)
history = model.fit(X_train, y_train, epochs=30,
                    validation_data=(X_valid, y_valid),
                    callbacks=[checkpoint_cb, tensorboard_cb])

"""To start the TensorBoard server, one option is to open a terminal, if needed activate the virtualenv where you installed TensorBoard, go to this notebook's directory, then type:

```bash
$ tensorboard --logdir=./my_logs --port=6006
```

You can then open your web browser to [localhost:6006](http://localhost:6006) and use TensorBoard. Once you are done, press Ctrl-C in the terminal window, this will shutdown the TensorBoard server.

Alternatively, you can load TensorBoard's Jupyter extension and run it like this:
"""

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard
# %tensorboard --logdir=./my_logs --port=6006

run_logdir2 = get_run_logdir()
run_logdir2

keras.backend.clear_session()
np.random.seed(42)
tf.random.set_seed(42)

model = keras.models.Sequential([
    keras.layers.Dense(30, activation="relu", input_shape=[8]),
    keras.layers.Dense(30, activation="relu"),
    keras.layers.Dense(1)
])    
model.compile(loss="mse", optimizer=keras.optimizers.SGD(lr=0.05))

tensorboard_cb = keras.callbacks.TensorBoard(run_logdir2)
history = model.fit(X_train, y_train, epochs=30,
                    validation_data=(X_valid, y_valid),
                    callbacks=[checkpoint_cb, tensorboard_cb])

"""Notice how TensorBoard now sees two runs, and you can compare the learning curves.

Check out the other available logging options:
"""

help(keras.callbacks.TensorBoard.__init__)

"""# Hyperparameter Tuning"""

keras.backend.clear_session()
np.random.seed(42)
tf.random.set_seed(42)

def build_model(n_hidden=1, n_neurons=30, learning_rate=3e-3, input_shape=[8]):
    model = keras.models.Sequential()
    model.add(keras.layers.InputLayer(input_shape=input_shape))
    for layer in range(n_hidden):
        model.add(keras.layers.Dense(n_neurons, activation="relu"))
    model.add(keras.layers.Dense(1))
    optimizer = keras.optimizers.SGD(lr=learning_rate)
    model.compile(loss="mse", optimizer=optimizer)
    return model

keras_reg = keras.wrappers.scikit_learn.KerasRegressor(build_model)

keras_reg.fit(X_train, y_train, epochs=100,
              validation_data=(X_valid, y_valid),
              callbacks=[keras.callbacks.EarlyStopping(patience=10)])

mse_test = keras_reg.score(X_test, y_test)

y_pred = keras_reg.predict(X_new)

np.random.seed(42)
tf.random.set_seed(42)

"""**Warning**: the following cell crashes at the end of training. This seems to be caused by [Keras issue #13586](https://github.com/keras-team/keras/issues/13586), which was triggered by a recent change in Scikit-Learn. [Pull Request #13598](https://github.com/keras-team/keras/pull/13598) seems to fix the issue, so this problem should be resolved soon. In the meantime, I've added `.tolist()` and `.rvs(1000).tolist()` as workarounds."""

from scipy.stats import reciprocal
from sklearn.model_selection import RandomizedSearchCV

param_distribs = {
    "n_hidden": [0, 1, 2, 3],
    "n_neurons": np.arange(1, 100)               .tolist(),
    "learning_rate": reciprocal(3e-4, 3e-2)      .rvs(1000).tolist(),
}

rnd_search_cv = RandomizedSearchCV(keras_reg, param_distribs, n_iter=10, cv=3, verbose=2)
rnd_search_cv.fit(X_train, y_train, epochs=100,
                  validation_data=(X_valid, y_valid),
                  callbacks=[keras.callbacks.EarlyStopping(patience=10)])

rnd_search_cv.best_params_

rnd_search_cv.best_score_

rnd_search_cv.best_estimator_

rnd_search_cv.score(X_test, y_test)

model = rnd_search_cv.best_estimator_.model
model

model.evaluate(X_test, y_test)