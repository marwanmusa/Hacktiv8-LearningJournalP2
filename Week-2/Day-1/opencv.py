# -*- coding: utf-8 -*-
"""d1pm_opencv.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/ardhiraka/FSDS_Guidelines/blob/master/p2/w2/d1pm_opencv.ipynb

# Face Recognition with OpenCV

First, clone this [repository](https://github.com/ardhiraka/ftds_face_recog). Add dataset folder and images folder, fill with your photos.

```dir
.
├── dataset
│   ├── raka [6 images]
│   ├── anggie [6 images]
│   └── unknown [6 images]
├── images
│   ├── raka.jpg
│   ├── unknown.jpg
│   └── anggie_raka.jpg
├── face_detection_model
│   ├── deploy.prototxt
│   └── res10_300x300_ssd_iter_140000.caffemodel
├── output
│   ├── embeddings.pickle
│   ├── le.pickle
│   └── recognizer.pickle
├── extract_embeddings.py
├── openface.nn4.small2.v1.t7
├── train_model.py
├── recognize.py
└── recognize_video.py
```

This project has four directories in the root folder:

- dataset/ : Contains our face images organized into subfolders by name.
- images/ : Contains three test images that we’ll use to verify the operation of our model.
- face_recognition_model/ : Contains a pre-trained Caffe deep learning model provided by OpenCV to detect faces. This model detects and localizes faces in an image.
- output/ : Contains my output pickle files. If you’re working with your own dataset, you can store your output files here as well. The output files include:
- embeddings.pickle : A serialized facial embeddings file. Embeddings have been computed for every face in the dataset and are stored in this file.
- le.pickle : Our label encoder. Contains the name labels for the people that our model can recognize.
- recognizer.pickle : Our Linear Support Vector Machine (SVM) model. This is a machine learning model rather than a deep learning model and it is responsible for actually recognizing faces.

Let’s summarize the five files in the root directory:

- extract_embeddings.py : We’ll review this file in Step #1 which is responsible for using a deep learning feature extractor to generate a 128-D vector describing a face. All faces in our dataset will be passed through the neural network to generate embeddings.
- openface_nn4.small2.v1.t7 : A Torch deep learning model which produces the 128-D facial embeddings. We’ll be using this deep learning model in Steps #1, #2, and #3.
- train_model.py : Our Linear SVM model will be trained by this script in Step #2. We’ll detect faces, extract embeddings, and fit our SVM model to the embeddings data.
- recognize.py : In Step #3 and we’ll recognize faces in images. We’ll detect faces, extract embeddings, and query our SVM model to determine who is in an image. We’ll draw boxes around faces and annotate each box with a name.
- recognize_video.py : How to recognize who is in frames of a video stream just as we did in Step #3 on static images.

## Step #1: Extract embeddings from face dataset

Now that we understand how face recognition works and reviewed our project structure, let’s get started building our OpenCV face recognition pipeline.

Before that, we have to install some library:

```shell
pip install opencv-python

pip install --upgrade imutils
```

Open up the `extract_embeddings.py` file and insert the following code:
"""

# import the necessary packages
from imutils import paths
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
	help="path to input directory of faces + images")
ap.add_argument("-e", "--embeddings", required=True,
	help="path to output serialized db of facial embeddings")
ap.add_argument("-d", "--detector", required=True,
	help="path to OpenCV's deep learning face detector")
ap.add_argument("-m", "--embedding-model", required=True,
	help="path to OpenCV's deep learning face embedding model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

"""Next, we process our command line arguments:

- --dataset : The path to our input dataset of face images.
- --embeddings : The path to our output embeddings file. Our script will compute face embeddings which we’ll serialize to disk.
- --detector : Path to OpenCV’s Caffe-based deep learning face detector used to actually localize the faces in the images.
- --embedding-model : Path to the OpenCV deep learning Torch embedding model. This model will allow us to extract a 128-D facial embedding vector.
- --confidence : Optional threshold for filtering week face detections.

Now that we’ve imported our packages and parsed command line arguments, lets load the face detector and embedder from disk:

"""

# load our serialized face detector from disk
print("[INFO] loading face detector...")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"],
	"res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
# load our serialized face embedding model from disk
print("[INFO] loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])

"""Here we load the face detector and embedder:

- detector : Loaded via Lines 3-6. We’re using a Caffe based DL face detector to localize faces in an image.
- embedder : Loaded on Line 9. This model is Torch-based and is responsible for extracting facial embeddings via deep learning feature extraction.

Notice that we’re using the respective cv2.dnn functions to load the two separate models.

Moving forward, let’s grab our image paths and perform initializations:

"""

# grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))
# initialize our lists of extracted facial embeddings and
# corresponding people names
knownEmbeddings = []
knownNames = []
# initialize the total number of faces processed
total = 0

"""The imagePaths list, built on Line 3, contains the path to each image in the dataset. I’ve made this easy via my imutils function, paths.list_images .

Our embeddings and corresponding names will be held in two lists: knownEmbeddings and knownNames (Lines 6 and 7).

We’ll also be keeping track of how many faces we’ve processed via a variable called total (Line 9).

Let’s begin looping over the image paths — this loop will be responsible for extracting embeddings from faces found in each image:

"""

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# extract the person name from the image path
	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]
	# load the image, resize it to have a width of 600 pixels (while
	# maintaining the aspect ratio), and then grab the image
	# dimensions
	image = cv2.imread(imagePath)
	image = imutils.resize(image, width=600)
	(h, w) = image.shape[:2]

"""We begin looping over imagePaths on Line 2.

First, we extract the name of the person from the path (Line 6). To explain how this works, consider the following example in my Python shell:

```shell
$ python
>>> from imutils import paths
>>> import os
>>> imagePaths = list(paths.list_images("dataset"))
>>> imagePath = imagePaths[0]
>>> imagePath
'dataset/raka/00004.jpg'
>>> imagePath.split(os.path.sep)
['dataset', 'raka', '00004.jpg']
>>> imagePath.split(os.path.sep)[-2]
'raka'
>>>
```

Notice how by using imagePath.split and providing the split character (the OS path separator — “/” on unix and “\” on Windows), the function produces a list of folder/file names (strings) which walk down the directory tree. We grab the second-to-last index, the persons name , which in this case is `raka` .

Finally, we wrap up the above code block by loading the image and resize it to a known width (Lines 10 and 11).

Let’s detect and localize faces:

"""

# construct a blob from the image
	imageBlob = cv2.dnn.blobFromImage(
		cv2.resize(image, (300, 300)), 1.0, (300, 300),
		(104.0, 177.0, 123.0), swapRB=False, crop=False)
	# apply OpenCV's deep learning-based face detector to localize
	# faces in the input image
	detector.setInput(imageBlob)
	detections = detector.forward()

"""On Lines 2-4, we construct a blob.

From there we detect faces in the image by passing the imageBlob through the detector network (Lines 7-8).

Let’s process the detections :

"""

# ensure at least one face was found
	if len(detections) > 0:
		# we're making the assumption that each image has only ONE
		# face, so find the bounding box with the largest probability
		i = np.argmax(detections[0, 0, :, 2])
		confidence = detections[0, 0, i, 2]
		# ensure that the detection with the largest probability also
		# means our minimum probability test (thus helping filter out
		# weak detections)
		if confidence > args["confidence"]:
			# compute the (x, y)-coordinates of the bounding box for
			# the face
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			# extract the face ROI and grab the ROI dimensions
			face = image[startY:endY, startX:endX]
			(fH, fW) = face.shape[:2]
			# ensure the face width and height are sufficiently large
			if fW < 20 or fH < 20:
				continue

"""The detections list contains probabilities and coordinates to localize faces in an image.

Assuming we have at least one detection, we’ll proceed into the body of the if-statement (Line 2).

We make the assumption that there is only one face in the image, so we extract the detection with the highest confidence and check to make sure that the confidence meets the minimum probability threshold used to filter out weak detections (Lines 5-10).

Assuming we’ve met that threshold, we extract the face ROI and grab/check dimensions to make sure the face ROI is sufficiently large (Lines 13-20).

From there, we’ll take advantage of our embedder CNN and extract the face embeddings:

"""

# construct a blob for the face ROI, then pass the blob
			# through our face embedding model to obtain the 128-d
			# quantification of the face
			faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
				(96, 96), (0, 0, 0), swapRB=True, crop=False)
			embedder.setInput(faceBlob)
			vec = embedder.forward()
			# add the name of the person + corresponding face
			# embedding to their respective lists
			knownNames.append(name)
			knownEmbeddings.append(vec.flatten())
			total += 1

"""We construct another blob, this time from the face ROI (not the whole image as we did before) on Lines 4-5.

Subsequently, we pass the faceBlob through the embedder CNN (Lines 6-7). This generates a 128-D vector (vec ) which describes the face. We’ll leverage this data to recognize new faces via machine learning.

And then we simply add the name and embedding vec to knownNames and knownEmbeddings , respectively (Lines 10-11).

We also can’t forget about the variable we set to track the total number of faces either — we go ahead and increment the value on Line 12.

We continue this process of looping over images, detecting faces, and extracting face embeddings for each and every image in our dataset.

All that’s left when the loop finishes is to dump the data to disk:

"""

# dump the facial embeddings + names to disk
print("[INFO] serializing {} encodings...".format(total))
data = {"embeddings": knownEmbeddings, "names": knownNames}
f = open(args["embeddings"], "wb")
f.write(pickle.dumps(data))
f.close()

"""We add the name and embedding data to a dictionary and then serialize the data in a pickle file on Lines 2-6.

At this point we’re ready to extract embeddings by running our script.

From there, open up a terminal and execute the following command to compute the face embeddings with OpenCV:

```shell
python extract_embeddings.py --dataset dataset --embeddings output/embeddings.pickle --detector face_recognition_model --embedding-model openface.nn4.small2.v1.t7
```

## Step #2: Train face recognition model

At this point we have extracted 128-d embeddings for each face — but how do we actually recognize a person based on these embeddings? The answer is that we need to train a “standard” machine learning model (such as an SVM, k-NN classifier, Random Forest, etc.) on top of the embeddings.

Open up the `train_model.py` file and insert the following code:
"""

# import the necessary packages
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import argparse
import pickle
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--embeddings", required=True,
	help="path to serialized db of facial embeddings")
ap.add_argument("-r", "--recognizer", required=True,
	help="path to output model trained to recognize faces")
ap.add_argument("-l", "--le", required=True,
	help="path to output label encoder")
args = vars(ap.parse_args())

"""We import our packages and modules on Lines 2-5. We’ll be using scikit-learn’s implementation of Support Vector Machines (SVM), a common machine learning model.

From there we parse our command line arguments:

- --embeddings : The path to the serialized embeddings (we exported it by running the previous extract_embeddings.py script).
- --recognizer : This will be our output model that recognizes faces. It is based on SVM. We’ll be saving it so we can use it in the next two recognition scripts.
- --le : Our label encoder output file path. We’ll serialize our label encoder to disk so that we can use it and the recognizer model in our image/video face recognition scripts.

Each of these arguments is required.

Let’s load our facial embeddings and encode our labels:

"""

# load the face embeddings
print("[INFO] loading face embeddings...")
data = pickle.loads(open(args["embeddings"], "rb").read())
# encode the labels
print("[INFO] encoding labels...")
le = LabelEncoder()
labels = le.fit_transform(data["names"])

"""Here we load our embeddings from Step #1 on Line 19. We won’t be generating any embeddings in this model training script — we’ll use the embeddings previously generated and serialized.

Then we initialize our scikit-learn LabelEncoder and encode our name labels (Lines 6-7).

Now it’s time to train our SVM model for recognizing faces:

"""

# train the model used to accept the 128-d embeddings of the face and
# then produce the actual face recognition
print("[INFO] training model...")
recognizer = SVC(C=1.0, kernel="linear", probability=True)
recognizer.fit(data["embeddings"], labels)

"""On Line 4 we initialize our SVM model, and on Line 5 we fit the model (also known as “training the model”).

Here we are using a Linear Support Vector Machine (SVM) but you can try experimenting with other machine learning models if you so wish.

After training the model we output the model and label encoder to disk as pickle files.

"""

# write the actual face recognition model to disk
f = open(args["recognizer"], "wb")
f.write(pickle.dumps(recognizer))
f.close()
# write the label encoder to disk
f = open(args["le"], "wb")
f.write(pickle.dumps(le))
f.close()

"""We write two pickle files to disk in this block — the face recognizer model and the label encoder.

At this point, be sure you executed the code from Step #1 first.

Now that we have finished coding train_model.py as well, let’s apply it to our extracted face embeddings:

```shell
python train_model.py --embeddings output/embeddings.pickle --recognizer output/recognizer.pickle --le output/le.pickle
```

Here you can see that our SVM has been trained on the embeddings and both the (1) SVM itself and (2) the label encoding have been written to disk, enabling us to apply them to input images and video.

## Step #3: Recognize faces with OpenCV

We are now ready to perform face recognition with OpenCV!

We’ll start with recognizing faces in images in this section and then move on to recognizing faces in video streams in the following section.

Open up the recognize.py file in your project and insert the following code:
"""

# import the necessary packages
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-d", "--detector", required=True,
	help="path to OpenCV's deep learning face detector")
ap.add_argument("-m", "--embedding-model", required=True,
	help="path to OpenCV's deep learning face embedding model")
ap.add_argument("-r", "--recognizer", required=True,
	help="path to model trained to recognize faces")
ap.add_argument("-l", "--le", required=True,
	help="path to label encoder")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

"""We import our required packages on Lines 2-7. At this point, you should have each of these packages installed.

Our six command line arguments are parsed on Lines 9-22:

- --image : The path to the input image. We will attempt to recognize the faces in this image.
- --detector : The path to OpenCV’s deep learning face detector. We’ll use this model to detect where in the image the face ROIs are.
- --embedding-model : The path to OpenCV’s deep learning face embedding model. We’ll use this model to extract the 128-D face embedding from the face ROI — we’ll feed the data into the recognizer.
- --recognizer : The path to our recognizer model. We trained our SVM recognizer in Step #2. This is what will actually determine who a face is.
- --le : The path to our label encoder. This contains our face labels such as 'raka' or 'anggie' .
- --confidence : The optional threshold to filter weak face detections.

Be sure to study these command line arguments — it is important to know the difference between the two deep learning models and the SVM model. If you find yourself confused later in this script, you should refer back to here.

Now that we’ve handled our imports and command line arguments, let’s load the three models from disk into memory:

"""

# load our serialized face detector from disk
print("[INFO] loading face detector...")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"],
	"res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
# load our serialized face embedding model from disk
print("[INFO] loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])
# load the actual face recognition model along with the label encoder
recognizer = pickle.loads(open(args["recognizer"], "rb").read())
le = pickle.loads(open(args["le"], "rb").read())

"""We load three models in this block. At the risk of being redundant, I want to explicitly remind you of the differences among the models:

- detector : A pre-trained Caffe DL model to detect where in the image the faces are (Lines 3-6).
- embedder : A pre-trained Torch DL model to calculate our 128-D face embeddings (Line 9).
- recognizer : Our Linear SVM face recognition model (Line 11). We trained this model in Step 2.

We also load our label encoder which holds the names of the people our model can recognize (Line 12).

Now let’s load our image and detect faces:

"""

# load the image, resize it to have a width of 600 pixels (while
# maintaining the aspect ratio), and then grab the image dimensions
image = cv2.imread(args["image"])
image = imutils.resize(image, width=600)
(h, w) = image.shape[:2]
# construct a blob from the image
imageBlob = cv2.dnn.blobFromImage(
	cv2.resize(image, (300, 300)), 1.0, (300, 300),
	(104.0, 177.0, 123.0), swapRB=False, crop=False)
# apply OpenCV's deep learning-based face detector to localize
# faces in the input image
detector.setInput(imageBlob)
detections = detector.forward()

"""Here we:

- Load the image into memory and construct a blob (Lines 3-9).
- Localize faces in the image via our detector (Lines 12-13).

Given our new detections , let’s recognize faces in the image. But first we need to filter weak detections and extract the face ROI:

"""

# loop over the detections
for i in range(0, detections.shape[2]):
	# extract the confidence (i.e., probability) associated with the
	# prediction
	confidence = detections[0, 0, i, 2]
	# filter out weak detections
	if confidence > args["confidence"]:
		# compute the (x, y)-coordinates of the bounding box for the
		# face
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")
		# extract the face ROI
		face = image[startY:endY, startX:endX]
		(fH, fW) = face.shape[:2]
		# ensure the face width and height are sufficiently large
		if fW < 20 or fH < 20:
			continue

"""You’ll recognize this block from Step #1. I’ll explain it here once more:

- We loop over the detections on Line 2 and extract the confidence of each on Line 5.
- Then we compare the confidence to the minimum probability detection threshold contained in our command line args dictionary, ensuring that the computed probability is larger than the minimum probability (Line 7).
- From there, we extract the face ROI (Lines 10-13) as well as ensure it’s spatial dimensions are sufficiently large (Lines 16-17).

Recognizing the name of the face ROI requires just a few steps:

"""

# construct a blob for the face ROI, then pass the blob
		# through our face embedding model to obtain the 128-d
		# quantification of the face
		faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
			(0, 0, 0), swapRB=True, crop=False)
		embedder.setInput(faceBlob)
		vec = embedder.forward()
		# perform classification to recognize the face
		preds = recognizer.predict_proba(vec)[0]
		j = np.argmax(preds)
		proba = preds[j]
		name = le.classes_[j]

"""First, we construct a faceBlob (from the face ROI) and pass it through the embedder to generate a 128-D vector which describes the face (Lines 4-7)

Then, we pass the vec through our SVM recognizer model (Line 9), the result of which is our predictions for who is in the face ROI.

We take the highest probability index (Line 10) and query our label encoder to find the name (Line 12). In between, I extract the probability on Line 11.

Note: You cam further filter out weak face recognitions by applying an additional threshold test on the probability. For example, inserting if proba < T (where T is a variable you define) can provide an additional layer of filtering to ensure there are less false-positive face recognitions.

Now, let’s display OpenCV face recognition results:

"""

# draw the bounding box of the face along with the associated
		# probability
		text = "{}: {:.2f}%".format(name, proba * 100)
		y = startY - 10 if startY - 10 > 10 else startY + 10
		cv2.rectangle(image, (startX, startY), (endX, endY),
			(0, 0, 255), 2)
		cv2.putText(image, text, (startX, y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)

"""For every face we recognize in the loop (including the “unknown”) people:

- We construct a text string containing the name and probability on Line 3.
- And then we draw a rectangle around the face and place the text above the box (Lines 4-8).

And then finally we visualize the results on the screen until a key is pressed (Lines 10 and 11).

It is time to recognize faces in images with OpenCV!

To apply our OpenCV face recognition pipeline to my provided images (or your own dataset + test images).

From there, open up a terminal and execute the following command:

```shell
python recognize.py --detector face_recognition_model --embedding-model openface.nn4.small2.v1.t7 --recognizer output/recognizer.pickle --le output/le.pickle --image images/raka.png
```

## Recognize faces in video streams

Open up the recognize_video.py file and let’s get started:
"""

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--detector", required=True,
	help="path to OpenCV's deep learning face detector")
ap.add_argument("-m", "--embedding-model", required=True,
	help="path to OpenCV's deep learning face embedding model")
ap.add_argument("-r", "--recognizer", required=True,
	help="path to model trained to recognize faces")
ap.add_argument("-l", "--le", required=True,
	help="path to label encoder")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

"""Our imports are the same as the Step #3 section above, except for Lines 2 and 3 where we use the imutils.video module. We’ll use VideoStream to capture frames from our camera and FPS to calculate frames per second statistics.

The command line arguments are also the same except we aren’t passing a path to a static image via the command line. Rather, we’ll grab a reference to our webcam and then process the video. Refer to Step #3 if you need to review the arguments.

Our three models and label encoder are loaded here:
"""

# load our serialized face detector from disk
print("[INFO] loading face detector...")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"],
	"res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
# load our serialized face embedding model from disk
print("[INFO] loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])
# load the actual face recognition model along with the label encoder
recognizer = pickle.loads(open(args["recognizer"], "rb").read())
le = pickle.loads(open(args["le"], "rb").read())

"""Here we load face detector , face embedder model, face recognizer model (Linear SVM), and label encoder.

Again, be sure to refer to Step #3 if you are confused about the three models or label encoder.

Let’s initialize our video stream and begin processing frames:
"""

# initialize the video stream, then allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
# start the FPS throughput estimator
fps = FPS().start()
# loop over frames from the video file stream
while True:
	# grab the frame from the threaded video stream
	frame = vs.read()
	# resize the frame to have a width of 600 pixels (while
	# maintaining the aspect ratio), and then grab the image
	# dimensions
	frame = imutils.resize(frame, width=600)
	(h, w) = frame.shape[:2]
	# construct a blob from the image
	imageBlob = cv2.dnn.blobFromImage(
		cv2.resize(frame, (300, 300)), 1.0, (300, 300),
		(104.0, 177.0, 123.0), swapRB=False, crop=False)
	# apply OpenCV's deep learning-based face detector to localize
	# faces in the input image
	detector.setInput(imageBlob)
	detections = detector.forward()

"""Our VideoStream object is initialized and started on Line 3. We wait for the camera sensor to warm up on Line 4.

We also initialize our frames per second counter (Line 6) and begin looping over frames on Line 8. We grab a frame from the webcam on Line 10.

From here everything is the same as Step 3. We resize the frame (Line 14) and then we construct a blob from the frame + detect where the faces are (Lines 17-23).

Now let’s process the detections:
"""

# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the prediction
		confidence = detections[0, 0, i, 2]
		# filter out weak detections
		if confidence > args["confidence"]:
			# compute the (x, y)-coordinates of the bounding box for
			# the face
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			# extract the face ROI
			face = frame[startY:endY, startX:endX]
			(fH, fW) = face.shape[:2]
			# ensure the face width and height are sufficiently large
			if fW < 20 or fH < 20:
				continue

"""Now it’s time to perform OpenCV face recognition:"""

# construct a blob for the face ROI, then pass the blob
			# through our face embedding model to obtain the 128-d
			# quantification of the face
			faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
				(96, 96), (0, 0, 0), swapRB=True, crop=False)
			embedder.setInput(faceBlob)
			vec = embedder.forward()
			# perform classification to recognize the face
			preds = recognizer.predict_proba(vec)[0]
			j = np.argmax(preds)
			proba = preds[j]
			name = le.classes_[j]
			# draw the bounding box of the face along with the
			# associated probability
			text = "{}: {:.2f}%".format(name, proba * 100)
			y = startY - 10 if startY - 10 > 10 else startY + 10
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				(0, 0, 255), 2)
			cv2.putText(frame, text, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
	# update the FPS counter
	fps.update()

"""Let’s display the results and clean up:"""

# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

"""To execute our OpenCV face recognition pipeline on a video stream, open up a terminal and execute the following command:

```shell
python recognize_video.py --detector face_recognition_model --embedding-model openface.nn4.small2.v1.t7 --recognizer output/recognizer.pickle --le output/le.pickle
```

"""