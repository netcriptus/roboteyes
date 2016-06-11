from webcolors import rgb_to_name

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
    # Get the colors
    import pdb; pdb.set_trace()
    colors = image["responses"][0]["imagePropertiesAnnotation"].get("dominantColors")
    print(colors)
    if not colors:
        return "I can't see any dominant color in here, put it closer please!"

    primary_color = colors[0]
    if primary_color["score"] <= 0.3:
        return "It seems to be quite colorful around here!"

    name = rgb_to_name((primary_color["color"][0], primary_color["color"][1], primary_color["color"][2]))
    return "It seem your {} is {}".format(query, name)


def is_there(query, image):
    return ''


query_classes = {'WhereIs': where_is,
                 'WhatDoYouSee': what_do_you_see,
                 'WhatColor': what_color,
                 'IsThere': is_there}
