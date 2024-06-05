#!/usr/bin/env python
# coding: utf-8

# <h2> Homework 6 </h2>

# Выполняла работу Куканова Абина, БКЛ-212

# In[2]:


#скачиваем все нужные библиотеки
import pandas as pd
from sklearn.model_selection import train_test_split
import re
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier


# In[ ]:


def clear_text(text):
    clear_text = re.sub(r'[^А-яЁё]+', ' ', text).lower()
    return " ".join(clear_text.split())



def clean_stop_words(text, stopwords):
    text = [word for word in text.split() if word not in stopwords]
    return " ".join(text)


# In[10]:


def pre_processing(comment):
    comment = re.sub(r'[^\w\s]','',comment)
    comment = comment.lower()
    comment = [lemmatizer.lemmatize(token) for token in comment.split(" ")]
    comment = [lemmatizer.lemmatize(token, "v") for token in comment]
    comment = [word for word in comment if not word in stop_words]
    comment = " ".join(comment)
    return comment


# In[3]:


joned_text = pd.read_csv('joined_bot.csv', delimiter=',')
train = pd.read_csv('train_bot.csv', delimiter=',')
test = pd.read_csv('test_bot.csv', delimiter = ',')


# In[5]:


stops = stopwords.words("english")
tfidf = TfidfVectorizer(stop_words=stops, binary=True, max_features=100)
tfidf.fit(joned_text['text'].values.astype('U'))
X_train = tfidf.transform(train['text'].values.astype('U'))
X_test = tfidf.transform(test['text'].values.astype('U'))


# Логистическая регрессия

# In[173]:


model = LogisticRegression()
model.fit(X_train, train['label'])
y_pred = model.predict(X_test)


# In[ ]:




