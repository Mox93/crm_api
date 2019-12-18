from models.company import Company as CompanyModel
from models.role import EmbeddedRole
from models.user import User
from .utils import DBInterface
from .role import Role, StrictRoleInput
from .product import ProductCategory
from graphene import ObjectType, Mutation, InputObjectType, String, Boolean, Field, List, InputField, ID, Int


class CommonAttributes(object):
    name = String()
    email = String()
    phone_number = String()
    roles = List(Role)
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

