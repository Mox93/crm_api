from datetime import datetime
from bson import ObjectId
from flask_mongoengine import MongoEngine


db = MongoEngine()

DB_NAME = "rizzmi_crm"
DB_PORT = 27017
DB_HOST = "localhost"


class ExtendedDocument(db.Document):
    """
    ...
    """

    meta = {"abstract": True}

    _id = db.ObjectIdField(primary_key=True, required=True, default=ObjectId)
    creation_date = db.DateTimeField()
    modified_date = db.DateTimeField(default=datetime.utcnow)

    def clean(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.utcnow()
        self.modified_date = datetime.utcnow()

    def json(self):
        result = self.to_mongo()

        for key, val in result.items():
            if isinstance(val, ObjectId):
                result[key] = str(val)
            elif isinstance(self[key], db.EmbeddedDocument):
                result[key] = self[key].json()
            elif isinstance(self[key], list):
                for i, item in enumerate(self[key]):
                    if isinstance(result[key][i], ObjectId):
                        result[key][i] = str(result[key][i])
                    elif isinstance(item, db.EmbeddedDocument):
                        result[key][i] = item.json()

        return result

    @classmethod
    def find_by_id(cls, _id):
        try:
            return cls.objects(_id=_id).first()
        except Exception as e:
            print(str(e))
            return

    @classmethod
    def find_one_by(cls, field_name, value):
        try:
            return cls.objects(**{field_name: value}).first()
        except Exception as e:
            print(str(e))
            return

    @classmethod
    def find_many_by(cls, field_name, value, sort_keys=tuple()):
        try:
            if sort_keys and isinstance(sort_keys, (tuple, list, set)):
                return list(cls.objects(**{field_name: value}).order_by(*sort_keys))
            return list(cls.objects(**{field_name: value}))
        except Exception as e:
            print(str(e))
            return []

    @classmethod
    def find_all(cls, sort_keys=tuple()):
        try:
            if sort_keys and isinstance(sort_keys, (tuple, list, set)):
                return list(cls.objects().order_by(*sort_keys))
            return list(cls.objects())
        except Exception as e:
            print(str(e))
            return []


class ExtendedEmbeddedDocument(db.EmbeddedDocument):
    """
    ...
    """

    meta = {"abstract": True}

    _id = db.ObjectIdField(required=True, default=ObjectId)
    creation_date = db.DateTimeField()
    modified_date = db.DateTimeField(default=datetime.utcnow)

    def clean(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.utcnow()
        self.modified_date = datetime.utcnow()

    def json(self):
        result = self.to_mongo()

        for key in result:
            if isinstance(result[key], ObjectId):
                result[key] = str(result[key])
            elif isinstance(self[key], db.EmbeddedDocument):
                result[key] = self[key].json()
            elif isinstance(self[key], list):
                for i, item in enumerate(self[key]):
                    if isinstance(result[key][i], ObjectId):
                        result[key][i] = str(result[key][i])
                    elif isinstance(item, db.EmbeddedDocument):
                        result[key][i] = item.json()

        return result

