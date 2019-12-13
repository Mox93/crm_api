from .role import EmbeddedRole
from . import db, ExtendedDocument


class User(ExtendedDocument):
    """
    ...
    """
    meta = {"collection": "users",
            "allow_inheritance": True}

    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)
    phone_number = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    company = db.ReferenceField('Company', reverse_delete_rule=3)
    role = db.EmbeddedDocumentListField(EmbeddedRole)

    def clean(self):

        if isinstance(self.first_name, str):
            self.first_name = self.first_name.lower()

        if isinstance(self.last_name, str):
            self.last_name = self.last_name.lower()

        if isinstance(self.email, str):
            self.email = self.email.lower()

    @classmethod
    def find_by_email(cls, email):
        return cls.objects(email=email.lower()).first()

    @classmethod
    def find_by_phone_number(cls, phone_number):
        return cls.objects(phone_number=phone_number.lower()).first()
