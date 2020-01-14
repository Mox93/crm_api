from .utils import DBInterface
from models.company import Company as CompanyModel
from models.product import Product as ProductModel
from .tag import ProductCategory, NewProductCategoryInput
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


class NewProductInput(InputObjectType):
    name = String(required=True)
    description = String()
    product_categories = List(NewProductCategoryInput)


class NewProduct(Mutation):
    class Meta:
        name = "NewProduct"
        description = "..."

    class Arguments:
        company_id = ID(required=True)
        product_data = NewProductInput(required=True)

    product = Field(lambda: Product)

    @staticmethod
    def mutate(root, info, company_id, product_data):
        company = CompanyModel.find_by_id(company_id)
        if not company:
            raise Exception("company doesn't exist!")

        product = ProductModel(**product_data, company=company_id)
        product.save()

        return NewProduct(product=product)


class NewProductFormInput(InputObjectType):
    pass


class NewProductForm(Mutation):
    class Meta:
        name = "ProductForm"
        description = "..."

    class Arguments:
        company_id = ID(required=True)
        product_form_data = NewProductFormInput(required=True)

    # TODO return something

    @staticmethod
    def mutate(root, info, company_id, product_form_data):
        # TODO write the body
        pass

