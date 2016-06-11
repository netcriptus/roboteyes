from random import shuffle

import nltk
from math import ceil
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.svm import SVC, LinearSVC, NuSVC

CLASS_WHAT_DO_YOU_SEE = "WhatDoYouSee"
ClASS_WHERE_IS = "WhereIs"

features = {
    CLASS_WHAT_DO_YOU_SEE: [
        "What do you see",
        "Can you see anything",
        "Tell me what's in this picture",
        "Is there anything",
        "Let me know what you see in this picture",

    ],
    ClASS_WHERE_IS: [
        "Where is",
        "Can you find",
        "Please find",
        "Is there a",
        "Is there"
    ]
}

labeled_sentences = []
for key, values in features.items():
    labeled_sentences += [(val, key) for val in values]

labeled_sentences += [
    ("It's to hot today", "Unknown"),
    ("What time is it", "Unknown"),
    ("Has anyone seen David?", "Unknown"),
    ("That is a bird", "Unknown"),
    ("Roboteyes is awesome", "Unkown"),
    ("What is your name", "Unknown")
]

def feature_set_for_input(input):
    for key, values in features.items():
        if input in values:
            return {'class': key}
    return {'class': 'Unknown'}

shuffle(labeled_sentences)

feature_sets = [(feature_set_for_input(sentence), gender) for (sentence, gender) in labeled_sentences]
cutting_point = ceil(len(feature_sets) * 0.7)
train_set, test_set = feature_sets[cutting_point:], feature_sets[:cutting_point]

classifiers = [MultinomialNB, BernoulliNB, LogisticRegression, SGDClassifier, SVC, LinearSVC, NuSVC]

if __name__ == "__main__":
    for clazz in classifiers:
        nltk_classifier = SklearnClassifier(clazz())
        nltk_classifier.train(train_set)
        print("{0} accuracy: {1}%".format(clazz.__name__, nltk.classify.accuracy(nltk_classifier, test_set)*100))