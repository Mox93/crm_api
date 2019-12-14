from graphene import Schema, ObjectType, List, Field, ID, String, Int, Boolean
from .user import Signup, Login
from .auth import Token, create_tokens
from .role import NewRole, Role
from .company import NewCompany, Company
from models.user import User as UserModel
from werkzeug.security import check_password_hash


class QueryType(ObjectType):
    class Meta:
        name = "Query"
        description = "..."

    login = Field(Login, email=String(required=True), password=String(required=True))

    @staticmethod
    def resolve_login(root, info, email, password):
        if email and password:
            user = UserModel.find_by_email(email)
            if user and check_password_hash(user.password, password):
                return Login(user=user, token=create_tokens(user))
            raise Exception("email or password were incorrect")


class MutationType(ObjectType):
    class Meta:
        name = "Mutation"
        description = "..."

    signup = Signup.Field()
    new_role = NewRole.Field()
    new_company = NewCompany.Field()


schema = Schema(query=QueryType, mutation=MutationType)
