from graphene import Schema, ObjectType, List, Field, ID, String, Int, Boolean
from .user import Signup, Login, AddMember
from .auth import Token, create_tokens
from .role import NewRole, Role, AddRoles
from .company import NewCompany, Company as CompanyType, AddProductCategory
from .product import NewProduct, Product as ProductType
from .tag import ProductCategory as ProductCategoryType
from .customer import Customer as CustomerType, AddCustomer
from .campaign import Campaign as CampaignType, NewCampaign
from models.campaign import Campaign as CampaignModel
from models.customer import Customer as CustomerModel
from models.user import User as UserModel
from models.company import Company as CompanyModel
from models.product import Product as ProductModel
from models.tag import ProductCategory as ProductCategoryModel
from werkzeug.security import check_password_hash


class QueryType(ObjectType):
    class Meta:
        name = "Query"
        description = "..."

    # User
    login = Field(Login, email=String(required=True), password=String(required=True))

    # Company
    company_list = List(CompanyType)

    # Product
    product_category_list = List(ProductCategoryType)
    product_category = Field(ProductCategoryType, _id=ID(required=True))
    product = Field(ProductType, _id=ID(required=True))
    product_list = List(ProductType, company_id=ID(required=True))

    # Contact
    customer = Field(CustomerType, _id=ID(required=True))
    customer_list = List(CustomerType, company_id=ID(required=True))

    # Campaign
    campaign = Field(CampaignType, _id=ID(required=True))
    campaign_list = List(CampaignType, company_id=ID(required=True))

    # RESOLVERS
    @staticmethod
    def resolve_login(root, info, email, password):
        user = UserModel.find_by_email(email)
        if user and check_password_hash(user.password, password):
            return Login(user=user, token=create_tokens(user))
        raise Exception("email or password were incorrect")

    @staticmethod
    def resolve_company_list(root, info):
        return CompanyModel.find_all()

    @staticmethod
    def resolve_product_category_list(root, info):
        return ProductCategoryModel.find_all()

    @staticmethod
    def resolve_product_category(root, info, _id):
        return ProductCategoryModel.find_by_id(_id)

    @staticmethod
    def resolve_product_list(root, info, company_id):
        return ProductModel.find_many_by(company_id)

    @staticmethod
    def resolve_product(root, info, _id):
        return ProductModel.find_by_id(_id)

    @staticmethod
    def resolve_customer(root, info, _id):
        return CustomerModel.find_by_id(_id)

    @staticmethod
    def resolve_customer_list(root, info, company_id):
        return CustomerModel.find_many_by(company_id)

    @staticmethod
    def resolve_campaign(root, info, _id):
        return CampaignModel.find_by_id(_id)

    @staticmethod
    def resolve_campaign_list(root, info, company_id):
        return CampaignModel.find_many_by(company_id)


class MutationType(ObjectType):
    class Meta:
        name = "Mutation"
        description = "..."

    # User
    signup = Signup.Field()
    add_member = AddMember.Field()

    # Company
    new_company = NewCompany.Field()
    new_role = NewRole.Field()  # TODO why do we need that???
    add_role = AddRoles.Field()

    # Product
    add_product_category = AddProductCategory.Field()
    new_product = NewProduct.Field()

    # Customer
    add_customer = AddCustomer.Field()

    # Campaign
    new_campaign = NewCampaign.Field()


schema = Schema(query=QueryType, mutation=MutationType)

