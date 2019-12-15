from .utils import DBInterface
from .field import EmbeddedFieldType
from graphene import ObjectType, Mutation, InputObjectType, String, Boolean, Field, List, InputField, ID


class CommonAttributes(object):
    pass


class ProductTemplate(ObjectType):
    class Meta:
        name = "ProductTemplate"
        description = "..."

    name = String()
    description = String()
    fields = List(EmbeddedFieldType)


class ProductTemplateInput(InputObjectType):
    pass

