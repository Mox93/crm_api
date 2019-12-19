from . import db, ExtendedDocument
from .company import Company
from .product import Product


class Campaign(ExtendedDocument):
    """
    ...
    """
    meta = {"collection": "campaigns"}

    name = db.StringField(required=True)
    description = db.StringField()
    product = db.LazyReferenceField(Product, required=True)
    platform = db.StringField()
    company = db.LazyReferenceField(Company, reverse_delete_rule=3, required=True)

