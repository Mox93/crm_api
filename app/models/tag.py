from . import db, ExtendedDocument


class Tag(ExtendedDocument):
    """
    ...
    """
    meta = {"collection": "tags",
            "allow_inheritance": True}

    name = db.StringField(required=True, unique=True)
    description = db.StringField()

    @classmethod
    def search_by_name(cls, name):
        return cls.objects(name__icontains=name)



class ProductCategory(Tag):
    pass

