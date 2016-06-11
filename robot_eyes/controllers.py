import requests
from watson_developer_cloud import VisualRecognitionV3, NaturalLanguageClassifierV1
from flask import Blueprint, request, Response, jsonify

import base64

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from wit import Wit
from .utils import analyze

controllers = Blueprint('controllers', __name__)


@controllers.route("/health", methods=["GET"])
def health():
    return "ok", 200


@controllers.route("/", methods=["POST"])
def index():
    if 'image' in request.files:
        image = request.files['image']
    else:
        image = request.form['image_url']
    question = request.form['question']

    result = query_google_vision_api(image)

    if "error" in result["responses"][0]:
        return jsonify("Please send me what you are seeing!")

    annotated_image = result['responses'][0]

    print(request.form)

    user_query = query_witai(question)
    response = analyze(user_query, annotated_image)

    return jsonify(response)


def query_google_vision_api(image):
    credentials = GoogleCredentials.get_application_default()
    discovery_url = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

    service = discovery.build('vision', 'v1', credentials=credentials,
                              discoveryServiceUrl=discovery_url)

    if isinstance(image, str):
        image_content = base64.b64encode(requests.get(image).raw.read())
    else:
        image_content = base64.b64encode(image.stream.read())
    print(image_content)
    service_request = service.images().annotate(body={
        'requests': [{
            'image': {'content': image_content.decode('UTF-8')},
            'features': [{'type': 'TYPE_UNSPECIFIED'},
                         {'type': 'LANDMARK_DETECTION'},
                         {'type': 'LOGO_DETECTION'},
                         {'type': 'LABEL_DETECTION'},
                         {'type': 'TEXT_DETECTION'},
                         {'type': 'IMAGE_PROPERTIES'}]
        }]
    })
    response = service_request.execute()
    return response


def query_witai(message):
    client = Wit('KZSEARP55DDI6JPLDNHJHWBKQKECHWGH', {})
    return client.message(message)
