from . import db, ExtendedDocument, ExtendedEmbeddedDocument
from models.field import EmbeddedFieldModel
from models.collection import CollectionTemplate, Reference


class TextCard(ExtendedDocument):
    title = db.StringField(required=True, default="Untitled Form")
    description = db.StringField()


class FormTemplate(ExtendedDocument):
    """
    ...
    """
    meta = {'collection': 'forms'}

    # TODO divide the form visually into sections

    name = db.StringField(required=True, default="Untitled Form")
    title_card = db.EmbeddedDocumentField(TextCard)
    text_cards = db.EmbeddedDocumentListField(TextCard)
    fields = db.EmbeddedDocumentListField(EmbeddedFieldModel)

    # form meta data
    collections = db.ListField(db.LazyReferenceField(CollectionTemplate, reverse_delete_rule=4))
    default_reference = db.EmbeddedDocumentField(Reference, required=True, default=Reference())
    links = db.ListField(db.ObjectIdField())

    def __init__(self, *args, **kwargs):
        super(FormTemplate, self).__init__(*args, **kwargs)
        self.foreign_fields_id = []

    def find_field_by_id(self, _id, index=False):
        for i, field in enumerate(self.fields):
            if _id == str(field._id):
                if index:
                    return i, field
                else:
                    return field
        if index:
            return -1, None


class FormMapModel(ExtendedDocument):
    """
    ...
    """
    meta = {'collection': 'forms_map'}

    form = db.ReferenceField(FormTemplate, reverse_delete_rule=2, required=True)  # , unique_with="values"
    # values = db.EmbeddedDocumentField()  # TODO must put something here

