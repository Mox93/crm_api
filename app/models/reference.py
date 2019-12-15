from . import db, ExtendedDocument, ExtendedEmbeddedDocument
from bson import ObjectId


class Reference(ExtendedEmbeddedDocument):
    """
    ...
    """

    name = db.StringField(required=True)
    description = db.StringField()
    collection = db.ObjectIdField(required=True, defualt=ObjectId)

