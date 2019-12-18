from .utils import DBInterface
from .company import Company as CompanyType
from models.company import Company as CompanyModel
from models.product import ProductCategory as ProductCategoryModel, Product as ProductModel
from graphene import ObjectType, Mutation, InputObjectType, String, Boolean, Field, List, InputField, ID


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


class AddProductCategory(Mutation):
    class Meta:
        name = "AddProductCategory"
        description = "..."

    class Arguments:
        company_id = ID(required=True)
        name = String(required=True)
        description = String()

    company = Field(lambda: CompanyType)

    @staticmethod
    def mutate(root, info, company_id, name, description=None):
        company = CompanyModel.find_by_id(company_id)
        if not company:
            raise Exception("Company doesn't exist!")

        product_category = ProductCategoryModel.find_one_by("name", name)
        if product_category:
            company.product_categories.append(product_category)
            company.save()

            return ProductCategory(company=company, product_category=product_category)

        product_category = ProductCategoryModel(name, description)
        product_category.save()

        company.product_categories.append(product_category)
        company.save()

        return ProductCategory(company=company)


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

