import json
from random import shuffle

import nltk
from math import ceil

import pickle

from fuzzywuzzy import fuzz
from nltk.classify.scikitlearn import SklearnClassifier
from nltk import word_tokenize, stem, tokenize, metrics
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.svm import SVC, LinearSVC, NuSVC
from watson_developer_cloud import NaturalLanguageClassifierV1, WatsonDeveloperCloudService

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
        "Where is in the picture",
        "Can you find in the picture",
        "Where is in the image",
        "Can you find in the image",
        "Please find in the picture",
        "Is there a here",
        "Is there",
        "Tell me where to find",
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
    ("Awesome is what awesome is", CLASS_UNKNOWN),
    ("Coloring  is not an option", CLASS_UNKNOWN),
    ("We have to admit that color looks weird", CLASS_UNKNOWN),
    ("No one knows where he is", CLASS_UNKNOWN)
]

stemmer = stem.PorterStemmer()


def normalize(s):
    words = tokenize.wordpunct_tokenize(s.lower().strip())
    return ' '.join([stemmer.stem(w) for w in words])


def fuzzy_match(s1, s2):
    return fuzz.ratio(normalize(s1), normalize(s2)) >= 80


def feature_set_for_input(input):
    tokens = word_tokenize(input)

    features = ["what .* color", "find", "see"]
    result = {}
    total_sum = 0
    for feature in features:
        result[feature] = sum([1 if fuzzy_match(t, feature) else 0 for t in tokens])
        total_sum += result[feature]

    # Add another feature that the sentence is not super long and only contains one item
    # result["total"] = total_sum/len(tokens)

    return result

shuffle(labeled_sentences)

feature_sets = [(feature_set_for_input(sentence), sentence_class) for (sentence, sentence_class) in labeled_sentences]
cutting_point = ceil(len(feature_sets) * 0.7)
train_set, test_set = feature_sets[cutting_point:], feature_sets[:cutting_point]

classifiers = [MultinomialNB, BernoulliNB, LogisticRegression, SGDClassifier, SVC, LinearSVC, NuSVC]


class RobotEyesNaturalLanguageClassifierV1(NaturalLanguageClassifierV1):
    default_url = 'https://gateway.watsonplatform.net/natural-language-classifier/api'

    def __init__(self, url=default_url, api_key=None):
        WatsonDeveloperCloudService.__init__(self, 'natural_language_classifier', url, api_key=api_key)

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description='Train a NLTK model to categorize input questions.')
    parser.add_argument('mode', type=str, help='The mode this script should run in')
    args = parser.parse_args()

    # if args.mode == "train":
    #     best_score = 0.0
    #     best_classifier = None
    #     for clazz in classifiers:
    #         nltk_classifier = SklearnClassifier(clazz())
    #         nltk_classifier.train(train_set)
    #
    #         score = nltk.classify.accuracy(nltk_classifier, test_set)
    #
    #         if score > best_score:
    #             best_classifier = nltk_classifier
    #             best_score = score
    #
    #         print("{0} accuracy: {1}%".format(clazz.__name__, score * 100))
    #
    #     # Save the best classifier that was found
    #     file = open("classifier.pickle", "wb")
    #     pickle.dump(best_classifier, file)
    #     file.close()
    # elif args.mode == "test":
    #     classifier = pickle.load(open("classifier.pickle", "rb"))
    #     while True:
    #         print(classifier.classify(feature_set_for_input(input("Give me some data:"))))

    natural_language_classifier = NaturalLanguageClassifierV1(username="d08848f4-f212-449c-8a70-e6918e8df154",
                                                              password="6wt2ixCv2Vkr")

    classifiers = natural_language_classifier.list()
    print(json.dumps(classifiers, indent=2))

    # create a classifier
    if args.mode == "train":
        with open('test.csv', 'rb') as training_data:
            print(json.dumps(natural_language_classifier.create(training_data=training_data, name='question'), indent=2))

    else:
        classes = natural_language_classifier.classify('2373f5x67-nlc-2355', input("Give me some data"))
        print(json.dumps(classes, indent=2))
