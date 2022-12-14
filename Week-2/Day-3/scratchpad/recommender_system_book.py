# -*- coding: utf-8 -*-
"""Recommender System Book.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ump_-5_RFTe9aFDZql1M3cqWecNrpqP7

# Collaborative Filtering
"""

import pandas as pd
from tensorflow.keras.layers import Input, Embedding, Flatten, Dot, Dense
from tensorflow.keras.models import Model
from sklearn.model_selection import train_test_split
import tensorflow as tf

books=pd.read_csv('https://raw.githubusercontent.com/Reinalynn/Building-a-Book-Recommendation-System-using-Python/master/books10k.csv')
ratings=pd.read_csv('https://raw.githubusercontent.com/Reinalynn/Building-a-Book-Recommendation-System-using-Python/master/ratings10k.csv')

books

ratings

ratings.book_id.max()

ratings.book_id.min()

train, val = train_test_split(ratings, test_size=0.1,random_state=42)
#train, test = train_test_split(train, test_size=0.2, random_state=42)

dim_books=ratings.book_id.max()+1
dim_users=ratings.user_id.max()+1


0 1 2 3 4 5 6

book_input = Input(shape=(1,), name="Book-Input")
book_embedding = Embedding(dim_books, 16, embeddings_initializer="he_normal",
            embeddings_regularizer=tf.keras.regularizers.l2(1e-6), name="Book-Embedding")(book_input)
book_vec = Flatten(name="Flatten-Books")(book_embedding)

user_input = Input(shape=(1,), name="User-Input")
user_embedding = Embedding(dim_users, 16, embeddings_initializer="he_normal",
            embeddings_regularizer=tf.keras.regularizers.l2(1e-6), name="User-Embedding")(user_input)
user_vec = Flatten(name="Flatten-Users")(user_embedding)

prod = Dot(name="Dot-Product", axes=1)([book_vec, user_vec])

dense = Dense(1,activation='relu')(prod)

model = Model([user_input, book_input], dense)
model.compile(loss='mean_squared_error',optimizer='adam')

model.summary()

Embedding(dim_books, 16, embeddings_initializer="he_normal",
            embeddings_regularizer=tf.keras.regularizers.l2(1e-6), name="Book-Embedding")(1)

tf.keras.utils.plot_model(model, show_shapes=True)

#X_train=train[['book_id','user_id']].values
y_train=(train.rating - ratings.rating.min()) / (ratings.rating.max() - ratings.rating.min())
y_val=(val.rating - ratings.rating.min()) / (ratings.rating.max() - ratings.rating.min())

history = model.fit(x=[train.user_id.values,train.book_id.values], 
                    y=y_train.values, 
                    batch_size=64, 
                    epochs=10, 
                    verbose=1, 
                    validation_data=([val.user_id.values,val.book_id.values], y_val.values))

import matplotlib.pyplot as plt

plt.plot(history.history["loss"])
plt.plot(history.history["val_loss"])
plt.title("model loss")
plt.ylabel("loss")
plt.xlabel("epoch")
plt.legend(["train", "test"], loc="upper left")
plt.show()

#Prediksi rekomendasi untuk user 1 - Buku Random
import numpy as np
num_books= 100

book_list = books.book_id.sample(num_books).values
user_1 = np.array([1 for i in range(len(book_list))])

pred = model.predict([user_1,book_list]).reshape(num_books)

top_5_ids = (-pred).argsort()[:5]
top_5_books_id = book_list[top_5_ids]
top_5_books_rating = pred[top_5_ids]*(ratings.rating.max() - ratings.rating.min()) + ratings.rating.min()


'''

user_1 | books
1         2893
1         234
1         12
1         100
1         224
'''

#Prediksi rekomendasi untuk user 1 - Buku random yang belum dibaca sama user 1
num_books= 100

book_list = ratings[ratings.user_id!=1].sample(num_books).book_id.values

user_1 = np.array([1 for i in range(len(book_list))])

pred = model.predict([user_1,book_list]).reshape(num_books)

top_5_ids = (-pred).argsort()[:5]
top_5_books_id = book_list[top_5_ids]
top_5_books_rating = pred[top_5_ids]*(ratings.rating.max() - ratings.rating.min()) + ratings.rating.min()

#Prediksi rekomendasi untuk user 1 - Buku yang populer random
num_books= 100

book_list = ratings.groupby('book_id').count().sort_values('user_id',ascending=False).index[:num_books]

user_1 = np.array([1 for i in range(len(book_list))])

pred = model.predict([user_1,book_list]).reshape(num_books)

top_5_ids = (-pred).argsort()[:5]
top_5_books_id = book_list[top_5_ids]
top_5_books_rating = pred[top_5_ids]*(ratings.rating.max() - ratings.rating.min()) + ratings.rating.min()



from PIL import Image
import urllib
from IPython.display import display, HTML

display(HTML('<h2>Lima Buku yang Disukai oleh User 1:</h2>'))

liked_books_user_1 = ratings[ratings.user_id==1].sort_values('rating',ascending=False).book_id[:5].values
user_rating = ratings[ratings.user_id==1].sort_values('rating',ascending=False).rating[:5].values
fig1,ax1=plt.subplots(ncols=5,figsize=(25,5))
for i,id in enumerate(liked_books_user_1):
  a=Image.open(urllib.request.urlopen(books['image_url'].loc[id]))
  ax1[i].imshow(a)
  ax1[i].set_title('{}\nRating: {}'.format(books['title'].loc[id],user_rating[i]))
  ax1[i].axis('off')

display(HTML('<h2>Lima Buku yang Direkomendasikan ke User 1:</h2>'))
fig2,ax2=plt.subplots(ncols=5,figsize=(25,5))
for i,id in enumerate(top_5_books_id):
  a=Image.open(urllib.request.urlopen(books['image_url'].loc[id]))
  ax2[i].imshow(a)
  ax2[i].set_title('{}\nrating: {:.0f}'.format(books['title'].loc[id],top_5_books_rating[i]))
  ax2[i].axis('off')

top_5_books_rating