import webcolors
from fuzzywuzzy import fuzz
from wand.image import Image

BAD_QUESTION = 'Can you rephrase that question?'
MIN_ACCURACY = 0.6


def analyze(user_query, annotated_image, raw_image):
    if 'category' not in user_query['entities']:
        print("Not enough confident for {}".format(user_query))
        return BAD_QUESTION

    if user_query['entities']['category'][0]['confidence'] < MIN_ACCURACY:
        print("Not enough confident for {}".format(user_query))
        return BAD_QUESTION

    query_class = user_query['entities']['category'][0]['value']
    search_query = None
    if 'search_query' in user_query['entities']:
        if user_query['entities']['search_query'][0]['confidence'] < MIN_ACCURACY:
            print("Not enough confident for {}".format(user_query))
            return BAD_QUESTION
        search_query = user_query['entities']['search_query'][0]['value']

    return query_classes[query_class].__call__(search_query, annotated_image, raw_image)


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


def center(min_pos, max_pos):
    distance = max_pos - min_pos
    return max_pos - distance/2


def where_is(query, image, raw_image):
    if "textAnnotations" not in image:
        return "Sorry, I can't find it right now :("

    descriptions = [item['description'].lower() for item in image['textAnnotations'][1:]]
    key = 'logoAnnotations' if 'logoAnnotations' in image else 'labelAnnotations'
    descriptions += [item['description'].lower() for item in image[key]]
    if not any(fuzz.partial_ratio(query.lower(), description) >= 70 for description in descriptions):
        return 'I could not find {} in this picture'.format(query)
    all_items = image['textAnnotations'][1:] + image[key]
    confidence = 0
    for item in all_items:
        match = fuzz.partial_ratio(item['description'].lower(), query.lower())
        if match >= 70 and match > confidence:
            item_position = item['boundingPoly']['vertices']
            confidence = match
    x_coord = [pos['x'] for pos in item_position]
    y_coord = [pos['y'] for pos in item_position]
    item_center = {'x': center(min(x_coord), max(x_coord)), 'y': center(min(y_coord), max(y_coord))}
    raw_image.seek(0)
    img = Image(file=raw_image)

    if item_center['y'] == img.page_height/2:
        vertical = 'center'
    elif item_center['y'] < img.page_height/2:
        vertical = 'upper'
    else:
        vertical = 'lower'

    if item_center['x'] == img.page_width/2:
        horizontal = 'center'
    elif item_center['x'] < img.page_width/2:
        horizontal = 'left'
    else:
        horizontal = 'right'

    return 'I see {0} on the {1} {2}'.format(query, vertical, horizontal)


def what_do_you_see(query, image, raw_image):
    key = 'logoAnnotations' if 'logoAnnotations' in image else 'labelAnnotations'
    items = [item['description'].lower() for item in image[key]]
    return 'I see:\n {}'.format('\n'.join(items))


def what_color(query, image, raw_image):
    # Get the colors
    colors = image["imagePropertiesAnnotation"].get("dominantColors")
    if not colors:
        return "I can't see any dominant color in here, put it closer please!"

    primary_color = colors["colors"][0]
    if primary_color["score"] <= 0.3:
        return "It seems to be quite colorful around here!"

    actual_color, closest_color = get_color_name((primary_color["color"]["red"], primary_color["color"]["green"],
                                                  primary_color["color"]["blue"]))

    if query:
        template = "It seems your {} is {}"
        if actual_color:
            return template.format(query, actual_color)
        else:
            return template.format(query, closest_color)
    else:
        template = "It seems this is {}"
        if actual_color:
            return template.format(actual_color)
        else:
            return template.format(closest_color)


def is_there(query, image, raw_image):
    descriptions = [item['description'].lower() for item in image['textAnnotations'][1:]]
    key = 'logoAnnotations' if 'logoAnnotations' in image else 'labelAnnotations'
    descriptions += [item['description'].lower() for item in image[key]]

    found = any(fuzz.partial_ratio(query.lower(), description) >= 70 for description in descriptions)
    return "Yes, got it!" if found else "No, I'm sorry ..."


def what_does_it_say(query, image, raw_image):
    if not 'textAnnotations' in image:
        return "Nothing :)"

    return " ".join([item["description"] for item in image["textAnnotations"]])


query_classes = {'WhereIs': where_is,
                 'WhatDoYouSee': what_do_you_see,
                 'WhatColor': what_color,
                 'IsThere': is_there,
                 "WhatDoesItSay": what_does_it_say}
