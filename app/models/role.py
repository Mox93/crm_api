from models import db, ExtendedEmbeddedDocument, ExtendedDocument


class Role(ExtendedDocument):
    """
    ...
    """
    meta = {"collection": "roles"}

    name = db.StringField(required=True, unique=True)
    description = db.StringField()
    # TODO rethink the structure
    group = db.IntField(required=True)  # , unique_with=["priority_level"])
    priority_level = db.IntField(required=True)  # , unique_with=["group"])

    # Embedded Document Version
    _embedded = None

    @classmethod
    def as_embedded(cls, *args, **kwargs):
        if not cls._embedded:
            cls._embedded = type("EmbeddedRole", (ExtendedEmbeddedDocument,),
                                 {"name": db.StringField(required=True),
                                  "description": cls.description,
                                  "group": cls.group,
                                  "priority_level": cls.priority_level})

        if args or kwargs:
            return cls._embedded(*args, **kwargs)

        return cls._embedded


EmbeddedRole = Role.as_embedded()
