import webcolors
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


def closest_color(requested_color):
    min_colors = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]


def get_color_name(requested_color):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_color)
    except ValueError:
        closest_name = closest_color(requested_color)
        actual_name = None
    return actual_name, closest_name


def where_is(query, image):
    return ''


def what_do_you_see(query, image):
    key = 'logoAnnotations' if 'logoAnnotations' in image else 'labelAnnotations'
    items = [item['description'].lower() for item in image[key]]
    return 'I see the following:\n {}'.format('\n'.join(items))


def what_color(query, image):
    # Get the colors
    colors = image["responses"][0]["imagePropertiesAnnotation"].get("dominantColors")
    if not colors:
        return "I can't see any dominant color in here, put it closer please!"

    primary_color = colors["colors"][0]
    if primary_color["score"] <= 0.3:
        return "It seems to be quite colorful around here!"

    actual_color, closest_color = get_color_name((primary_color["color"]["red"], primary_color["color"]["green"],
                                                  primary_color["color"]["blue"]))
    template = "It seem your {} is {}"
    if actual_color:
        return template.format(query, actual_color)
    else:
        return template.format(query, closest_color)


def is_there(query, image):
    descriptions = [item['description'].lower() for item in image['textAnnotations'][1:]]
    descriptions += [item['description'].lower() for item in image['logoAnnotations']]
    query_terms = query.split()
    return any(term.lower() in descriptions for term in query_terms)


query_classes = {'WhereIs': where_is,
                 'WhatDoYouSee': what_do_you_see,
                 'WhatColor': what_color,
                 'IsThere': is_there}
