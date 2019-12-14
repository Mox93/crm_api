from models.role import Role as RoleModel
from .utils import DBInterface
from graphene import ObjectType, Mutation, InputObjectType, String, Boolean, Field, List, Int


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
