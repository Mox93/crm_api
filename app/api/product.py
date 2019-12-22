from .utils import DBInterface
from models.company import Company as CompanyModel
from models.product import Product as ProductModel
from .tag import ProductCategory, StrictProductCategoryInput
from graphene import ObjectType, Mutation, InputObjectType, String, Field, List, ID


class CommonAttributes(object):
    name = String()
    description = String()


class ProductInterface(CommonAttributes, DBInterface):
    company = ID()
    product_categories = List(ProductCategory)


class Product(ObjectType):
    class Meta:
        name = "Product"
        description = "..."
        interfaces = (ProductInterface,)


class StrictProductInput(InputObjectType):
    name = String(required=True)
    description = String()
    product_categories = List(StrictProductCategoryInput)


class NewProduct(Mutation):
    class Meta:
        name = "NewProduct"
        description = "..."

    class Arguments:
        company_id = ID(required=True)
        product_data = StrictProductInput(required=True)

    product = Field(lambda: Product)

    @staticmethod
    def mutate(root, info, company_id, product_data):
        company = CompanyModel.find_by_id(company_id)
        if not company:
            raise Exception("Company doesn't exist!")

        product = ProductModel(**product_data, company=company_id)
        product.save()

        return NewProduct(product=product)

