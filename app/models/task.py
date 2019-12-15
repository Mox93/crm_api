from models import ExtendedDocument, db


class Task(ExtendedDocument):
    """
    ...
    """
    meta = {"collection": "tasks",
            "allow_inheritance": True}

    name = db.StringField(required=True)
    priority = db.IntField(required=True)
    description = db.StringField()
    subject = db.ObjectIdField(required=True)

