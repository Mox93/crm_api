from .utils import DBInterface
from graphene import ObjectType, String, InputObjectType


class CommonAttributes(object):
    name = String()
    description = String()


class ProductCategoryInterface(CommonAttributes, DBInterface):
    pass


class ProductCategory(ObjectType):
    class Meta:
        name = "ProductCategory"
        description = "..."
        interfaces = (ProductCategoryInterface,)


class StrictProductCategoryInput(InputObjectType):
    name = String(required=True)
    description = String()

