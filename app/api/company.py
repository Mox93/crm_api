from models.company import Company as CompanyModel
from models.role import EmbeddedRole
from models.user import User
from models.tag import ProductCategory as ProductCategoryModel
from .utils import DBInterface
from .tag import ProductCategory, StrictProductCategoryInput
# from .role import Role, StrictRoleInput
from graphene import ObjectType, Mutation, InputObjectType, String, Boolean, Field, List, ID


class CommonAttributes(object):
    name = String()
    email = String()
    phone_number = String()
    # roles = List(Role)
    product_categories = List(ProductCategory)


class CompanyInterface(CommonAttributes, DBInterface):
    pass


class Company(ObjectType):
    class Meta:
        name = "Company"
        description = "..."
        interfaces = (CompanyInterface,)


class StrictCompanyInput(InputObjectType):
    name = String(required=True)
    email = String()
    phone_number = String()
    # roles = List(InputField(StrictRoleInput))


class NewCompany(Mutation):
    class Meta:
        name = "NewCompany"
        description = "..."

    class Arguments:
        company_data = StrictCompanyInput(required=True)
        user_id = ID()

    ok = Boolean()
    company = Field(lambda: Company)

    @staticmethod
    def mutate(root, info, company_data, user_id):
        name_check = CompanyModel.find_by_name(company_data.name)
        if name_check:
            raise Exception("Company already exist!")

        user = User.find_by_id(user_id)
        if user.company:
            raise Exception("User already belongs to a company!")

        owner_role = EmbeddedRole(name="owner", group=0, priority_level=0)

        company = CompanyModel(**company_data)
        company.roles.append(owner_role)
        company.save()

        user.role.append(owner_role)
        user.company = company
        user.save()

        return NewCompany(ok=True, company=company)


class AddProductCategory(Mutation):
    class Meta:
        name = "AddProductCategory"
        description = "..."

    class Arguments:
        company_id = ID(required=True)
        product_category_data = StrictProductCategoryInput(required=True)

    company = Field(lambda: Company)

    @staticmethod
    def mutate(root, info, company_id, product_category_data):
        company = CompanyModel.find_by_id(company_id)
        if not company:
            raise Exception("Company doesn't exist!")

        product_category = ProductCategoryModel.find_one_by("name", product_category_data.name)
        if product_category:
            company.product_categories.append(product_category)
            company.save()

            return ProductCategory(company=company, product_category=product_category)

        product_category = ProductCategoryModel(**product_category_data)
        product_category.save()

        company.product_categories.append(product_category)
        company.save()

        return ProductCategory(company=company)
