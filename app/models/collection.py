from bson import ObjectId
from . import db, ExtendedDocument, ExtendedEmbeddedDocument


class Reference(ExtendedEmbeddedDocument):
    """
    ...
    """
    # name = db.StringField(required=True, default="Untitled Collection")
    collection = db.ObjectIdField(required=True, defualt=ObjectId)
    dynamic = db.BooleanField(required=True, default=False)


class CollectionTemplate(ExtendedDocument):
    """
    ...
    """
    meta = {'collection': 'collection_templates'}

    name = db.StringField(required=True, default="Untitled Collection")
    title = db.StringField(required=True, default="Untitled Collection")
    description = db.StringField()
    fields = db.EmbeddedDocumentListField(ExtendedEmbeddedDocument)
    reference = db.EmbeddedDocumentField(Reference)

