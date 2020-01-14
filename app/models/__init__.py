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
    creation_date = db.DateTimeField(required=True)
    modified_date = db.DateTimeField(required=True, default=datetime.utcnow)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.utcnow()
        self.modified_date = datetime.utcnow()

        for key in self:
            if isinstance(self[key], db.EmbeddedDocument):
                self[key].save()
            if isinstance(self[key], list):
                for val in self[key]:
                    if isinstance(val, db.EmbeddedDocument):
                        val.save()

        super(ExtendedDocument, self).save(*args, **kwargs)

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
    creation_date = db.DateTimeField(required=True)
    modified_date = db.DateTimeField(required=True, default=datetime.utcnow)

    def save(self):
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


def create_field(data):
    field = DTYPES[data.data_type]
    return field(required=data.required, unique=data.unique)


def create_model(name, parents, attributes):
    return type(name, parents, {field.name: create_field(field) for field in attributes})


DTYPES = {"bool": db.BooleanField,
          "datetime": db.DateTimeField,
          "dict": db.DictField,
          "dynamic": db.DynamicField,
          "email": db.EmailField,
          "float": db.FloatField,
          "int": db.IntField,
          "list": db.ListField,
          "str": db.StringField}

ACCEPT_MAX_LEN = ["str", "list", "email"]
ACCEPT_MIN_LEN = ["str", "email"]
ACCEPT_MIN_VAL = ["int", "float"]
ACCEPT_MAX_VAL = ["int", "float"]
