#!/usr/bin/python

import pickle
import numpy
from sklearn import tree
from sklearn.metrics import accuracy_score
numpy.random.seed(42)


### The words (features) and authors (labels), already largely processed.
### These files should have been created from the previous (Lesson 10)
### mini-project.
words_file = "../text_learning/your_word_data.pkl" 
authors_file = "../text_learning/your_email_authors.pkl"
word_data = pickle.load( open(words_file, "r"))
authors = pickle.load( open(authors_file, "r") )

# Clean up word data
for i, words in enumerate(word_data):
    for skip in ['sshacklensf', 'cgermannsf']:
       words = words.replace(skip, '')
    word_data[i] = words


### test_size is the percentage of events assigned to the test set (the
### remainder go into training)
### feature matrices changed to dense representations for compatibility with
### classifier functions in versions 0.15.2 and earlier
from sklearn import cross_validation
features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(word_data, authors, test_size=0.1, random_state=42)

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                             stop_words='english')
features_train = vectorizer.fit_transform(features_train)
processed_words = vectorizer.get_feature_names()
features_test  = vectorizer.transform(features_test).toarray()


### a classic way to overfit is to use a small number
### of data points and a large number of features;
### train on only 150 events to put ourselves in this regime
features_train = features_train[:150].toarray()
labels_train   = labels_train[:150]



### your code goes here
clf = tree.DecisionTreeClassifier(min_samples_split=40)
clf.fit(features_train, labels_train)

important_features = []
pos = []
important_word = []
for i, imp in enumerate(clf.feature_importances_):
    if imp > 0.2:
        pos.append(i)
        important_features.append(imp)
        important_word.append(processed_words[i])

print "The important features are %s with importance at %s position %s" % (important_word, important_features, pos)

#Predict the test data
pred = clf.predict(features_test)

acc = accuracy_score(pred,labels_test)
print "Accuracy is {0}".format(acc)


