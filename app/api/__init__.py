from graphene import Schema, ObjectType, List, Field, ID, String, Int, Boolean
from .user import Signup, User as UserType
from .auth import Token, create_tokens
from models.user import User as UserModel
from werkzeug.security import check_password_hash


class QueryType(ObjectType):
    class Meta:
        name = "Query"
        description = "..."

    login = Field(Token, email=String(required=True), password=String(required=True))

    @staticmethod
    def resolve_login(root, info, email, password):
        if email and password:
            viewer = UserModel.find_by_email(email)
            if viewer and check_password_hash(viewer.password, password):
                return create_tokens(viewer)
            raise Exception("email or password were incorrect")


class MutationType(ObjectType):
    class Meta:
        name = "Mutation"
        description = "..."

    signup = Signup.Field()


schema = Schema(query=QueryType, mutation=MutationType)
