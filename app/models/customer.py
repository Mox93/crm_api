from . import db, ExtendedDocument
from .campaign import Company
from .campaign import Campaign


class Customer(ExtendedDocument):
    """
    ...
    """
    meta = {"collection": "customers"}

    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)
    phone_number = db.StringField(required=True, unique=True)
    company = db.LazyReferenceField(Company, reverse_delete_rule=2)
    source = db.ReferenceField(Campaign, reverse_delete_rule=0)

