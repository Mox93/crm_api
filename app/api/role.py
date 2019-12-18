from models.role import Role as RoleModel
from models.company import Company as CompanyModel
from models.role import EmbeddedRole
from .utils import DBInterface
from .company import Company as CompanyType
from graphene import ObjectType, Mutation, InputObjectType, String, Boolean, Field, List, Int, ID


class CommonAttributes(object):
    name = String()
    description = String()
    group = Int()
    priority_level = Int()


class RoleInterface(CommonAttributes, DBInterface):
    pass


class Role(ObjectType):
    class Meta:
        name = "Role"
        description = "..."
        interfaces = (RoleInterface,)


class StrictRoleInput(InputObjectType):
    name = String(required=True)
    description = String()
    group = Int(required=True)
    priority_level = Int(required=True)


class NewRole(Mutation):
    class Meta:
        name = "NewRole"
        description = "..."

    class Arguments:
        role_data = StrictRoleInput(required=True)

    ok = Boolean()
    role = Field(lambda: Role)

    @staticmethod
    def mutate(root, info, role_data):
        role = RoleModel(**role_data)
        role.save()
        return NewRole(ok=True, role=role)


class AddRoles(Mutation):
    class Meta:
        name = "AddRole"
        description = "..."

    class Arguments:
        company_id = ID(required=True)
        role_data = StrictRoleInput(required=True)

    company = Field(lambda: CompanyType)

    @staticmethod
    def mutate(root, info, company_id, role_data):
        company = CompanyModel.find_by_id(company_id)
        if not company:
            raise Exception("Company doesn't exist!")

        role = EmbeddedRole(**role_data)

        company.roles.append(role)
        company.save()

        return AddRoles(company=company)

