from . import db, ExtendedDocument


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

