from . import db, ExtendedDocument
from .role import EmbeddedRole
from .reference import Reference


class Company(ExtendedDocument):
    """
    ...
    """
    meta = {"collection": "companies",
            "allow_inheritance": True}

    name = db.StringField(required=True, unique=True)
    email = db.EmailField(unique=True, sparse=True)
    phone_number = db.StringField(unique=True, sparse=True)
    # team = db.ListField(db.ReferenceField(User, reverse_delete_rule=4), required=True)
    roles = db.EmbeddedDocumentListField(EmbeddedRole, required=True)

    # campaigns = db.EmbeddedDocumentField()  # Campaign
    # customers = db.EmbeddedDocumentField()  # Customer

    stuff = db.EmbeddedDocumentListField(Reference)

    @classmethod
    def find_by_name(cls, name):
        return cls.objects(name=name).first()
