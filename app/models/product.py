from . import db, ExtendedDocument
from .form import FormTemplate


class ProductCategory(ExtendedDocument):
    """
    ...
    """
    meta = {"collection": "product_categories"}

    name = db.StringField(required=True, unique=True)
    description = db.StringField()

    @classmethod
    def search_by_name(cls, name):
        return cls.objects(name__icontains=name)


from .company import Company


class ProductForm(FormTemplate):
    """
    ...
    """
    meta = {"collection": "product_forms"}

    company = db.LazyReferenceField(Company, reverse_delete_rule=2)
    product_categories = db.ListField(db.ReferenceField(ProductCategory, reverse_delete_rule=4))


class Product(ExtendedDocument):
    """
    ...
    """
    meta = {"collection": "products",
            "allow_inheritance": True}

    name = db.StringField(required=True)
    description = db.StringField()
    company = db.LazyReferenceField(Company, reverse_delete_rule=2, required=True)
    product_categories = db.ListField(db.ReferenceField(ProductCategory, reverse_delete_rule=4))

    @classmethod
    def find_by_category(cls, category_id):
        cls.objects(product_categories=category_id)

