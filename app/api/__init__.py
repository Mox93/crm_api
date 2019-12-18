from graphene import Schema, ObjectType, List, Field, ID, String, Int, Boolean
from .user import Signup, Login, AddMember
from .auth import Token, create_tokens
from .role import NewRole, Role, AddRoles
from .company import NewCompany, Company as CompanyType
from .product import ProductCategory as ProductCategoryType, AddProductCategory, NewProduct
from models.user import User as UserModel
from models.company import Company as CompanyModel
from models.product import ProductCategory as ProductCategoryModel, Product as ProductModel
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


class MutationType(ObjectType):
    class Meta:
        name = "Mutation"
        description = "..."

    # User
    signup = Signup.Field()

    # Company
    new_role = NewRole.Field()
    new_company = NewCompany.Field()

    add_product_category = AddProductCategory.Field()
    add_role = AddRoles.Field()
    add_member = AddMember.Field()

    # Product
    new_product = NewProduct.Field()


schema = Schema(query=QueryType, mutation=MutationType)

