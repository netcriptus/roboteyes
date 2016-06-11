from random import shuffle

import nltk
from math import ceil

import pickle
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.svm import SVC, LinearSVC, NuSVC

CLASS_WHAT_DO_YOU_SEE = "WhatDoYouSee"
ClASS_WHERE_IS = "WhereIs"
CLASS_WHAT_COLOR = "WhatColor"
CLASS_UNKNOWN = "Unknown"

features = {
    CLASS_WHAT_DO_YOU_SEE: [
        "What do you see",
        "Can you see anything",
        "Tell me what's in this picture",
        "Is there anything",
        "Let me know what you see in this picture",
        "Can you tell me what is in here?",
        "Is there anything you can see in there?"

    ],
    CLASS_WHAT_COLOR: [
        "What color is this",
        "Can you tell me the color of this",
        "Please tell me the color",
        "Tell me the color of this object",
    ],
    ClASS_WHERE_IS: [
        "Where is",
        "Can you find",
        "Please find",
        "Is there a",
        "Is there",
        "Tell me where",
        "Help me find"
    ]
}

labeled_sentences = []
for key, values in features.items():
    labeled_sentences += [(val, key) for val in values]

labeled_sentences += [
    ("It's to hot today", CLASS_UNKNOWN),
    ("What time is it", CLASS_UNKNOWN),
    ("Has anyone seen David?", CLASS_UNKNOWN),
    ("That is a bird", CLASS_UNKNOWN),
    ("Roboteyes is awesome", CLASS_UNKNOWN),
    ("What is your name", CLASS_UNKNOWN),
    ("What is the weather going to be tomorrow", CLASS_UNKNOWN),
    ("Birds are animals", CLASS_UNKNOWN),
    ("Plants are not", CLASS_UNKNOWN),
    ("Awesome is what awesome is", CLASS_UNKNOWN)
]

def feature_set_for_input(input):
    for key, values in features.items():
        if input in values:
            return {'class': key}
    return {'class': 'Unknown'}

shuffle(labeled_sentences)

feature_sets = [(feature_set_for_input(sentence), sentence_class) for (sentence, sentence_class) in labeled_sentences]
cutting_point = ceil(len(feature_sets) * 0.7)
train_set, test_set = feature_sets[cutting_point:], feature_sets[:cutting_point]

classifiers = [MultinomialNB, BernoulliNB, LogisticRegression, SGDClassifier, SVC, LinearSVC, NuSVC]

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Train a NLTK model to categorize input questions.')
    parser.add_argument('mode', type=str, help='The mode this script should run in')
    args = parser.parse_args()

    if args.mode == "train":
        best_score = 0.0
        best_classifier = None
        for clazz in classifiers:
            nltk_classifier = SklearnClassifier(clazz())
            nltk_classifier.train(train_set)

            score = nltk.classify.accuracy(nltk_classifier, test_set)

            if score > best_score:
                best_classifier = nltk_classifier
                best_score = score

            print("{0} accuracy: {1}%".format(clazz.__name__, score * 100))

        # Save the best classifier that was found
        file = open("classifier.pickle", "wb")
        pickle.dump(best_classifier, file)
        file.close()
    elif args.mode == "test":
        classifier = pickle.load(open("classifier.pickle", "rb"))
        while True:
            print(classifier.classify(feature_set_for_input(input("Give me some data:"))))