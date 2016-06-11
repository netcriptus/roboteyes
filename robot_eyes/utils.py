BAD_QUESTION = 'Can you rephrase that question?'
MIN_ACCURACY = 0.6


def analyze(user_query, annotated_image):
    if 'category' not in user_query['entities']:
        return BAD_QUESTION

    if user_query['entities']['category'][0]['confidence'] < MIN_ACCURACY:
        return BAD_QUESTION

    query_class = user_query['entities']['category'][0]['value']
    search_query = None
    if 'search_query' in user_query['entities']:
        if user_query['entities']['search_query'][0]['confidence'] < MIN_ACCURACY:
            return BAD_QUESTION
        search_query = user_query['entities']['search_query'][0]['value']

    return query_classes[query_class].__call__(search_query, annotated_image)


def where_is(query, image):
    return ''


def what_do_you_see(query, image):
    return ''


def what_color(query, image):
    return ''


def is_there(query, image):
    return ''


query_classes = {'WhereIs': where_is,
                 'WhatDoYouSee': what_do_you_see,
                 'WhatColor': what_color,
                 'IsThere': is_there}
