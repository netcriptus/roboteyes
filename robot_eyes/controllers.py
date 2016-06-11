from watson_developer_cloud import VisualRecognitionV3
from flask import Blueprint, request, Response

controllers = Blueprint('controllers', __name__)


@controllers.route("/health", methods=["GET"])
def health():
    return "ok", 200


@controllers.route("/", methods=["POST"])
def index():
    image = request.json['image']
    question = request.json['question']
    return Response()
