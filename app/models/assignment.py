from . import ExtendedDocument, db
from .task import Task
from .user import User


class Assignment(ExtendedDocument):
    """
    ...
    """
    meta = {"collection": "assignments",
            "allow_inheritance": True}

    task = db.ReferenceField(Task, required=True)
    manager = db.ReferenceField(User, required=True)
    status = db.StringField(required=True)
