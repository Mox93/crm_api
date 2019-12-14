from models.user import User as UserModel
from werkzeug.security import generate_password_hash
from .utils import DBInterface
from .auth import Token, create_tokens
from .role import Role
from graphene import ObjectType, Mutation, InputObjectType, String, Boolean, Field, ID, List


class CommonAttributes(object):
    first_name = String()
    last_name = String()
    email = String()
    phone_number = String()
    company = ID()
    role = List(Role)


class UserInterface(CommonAttributes, DBInterface):
    pass


class User(ObjectType):
    class Meta:
        name = "User"
        description = "..."
        interfaces = (UserInterface,)


class Login(ObjectType):
    class Meta:
        name = "Login"
        description = "..."

    user = Field(User)
    token = Field(Token)


class StrictUserInput(InputObjectType):
    first_name = String(required=True)
    last_name = String(required=True)
    email = String(required=True)
    phone_number = String(required=True)
    password = String(required=True)


class UserInput(CommonAttributes, InputObjectType):
    pass


class Signup(Mutation):
    class Meta:
        name = "Signup"
        description = "..."

    class Arguments:
        user_data = StrictUserInput(required=True)

    ok = Boolean()
    user = Field(lambda: User)
    token = Field(lambda: Token)

    @staticmethod
    def mutate(root, info, user_data):
        email_check = UserModel.find_by_email(user_data.email)
        if email_check:
            return Signup(ok=False)

        phone_number_check = UserModel.find_by_phone_number(user_data.phone_number)
        if phone_number_check:
            return Signup(ok=False)

        user = UserModel(**user_data)
        user.password = generate_password_hash(user_data.password, method="sha256")

        user.save()
        return Signup(ok=True, user=user, token=create_tokens(user))

