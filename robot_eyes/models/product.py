from robot_eyes import db
from robot_eyes.models import ModelMixin
from sqlalchemy.dialects.postgresql import JSON


class Product(db.Model, ModelMixin):
    id = db.Column(db.String(36), primary_key=True, default=uuid4().hex, autoincrement=False)
    description = db.Column(db.String(50))
    relative_position = db.Column(JSON())


class AnnotatedImage(db.Model, ModelMixin):
    id = db.Column(db.String(36), primary_key=True, default=uuid4().hex, autoincrement=False)
    dominant_colors = db.Column(JSON())
