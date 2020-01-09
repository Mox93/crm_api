from models.user import User as UserModel
from models.company import Company as CompanyModel
from werkzeug.security import generate_password_hash
from .utils import DBInterface
from .auth import Token, create_tokens
from .role import Role
from graphene import ObjectType, Mutation, InputObjectType, String, Boolean, Field, ID, List
from common.utils import send_email


class CommonAttributes(object):
    first_name = String(required=True)
    last_name = String(required=True)
    email = String(required=True)
    phone_number = String(required=True)


class UserInterface(CommonAttributes, DBInterface):
    company = ID()
    role = List(Role)

    @staticmethod
    def resolve_company(root, info):
        if root.company:
            return str(root.company.id)


class User(ObjectType):
    class Meta:
        name = "User"
        description = "..."
        interfaces = (UserInterface,)


class Login(ObjectType):
    class Meta:
        name = "Login"
        description = "..."

    user = Field(User, required=True)
    token = Field(Token, required=True)


class NewUserInput(CommonAttributes, InputObjectType):
    password = String(required=True)


class UserInput(InputObjectType):
    first_name = String()
    last_name = String()
    email = String()
    phone_number = String()
    company = ID()
    role = List(Role)


class Signup(Mutation):
    class Meta:
        name = "Signup"
        description = "..."

    class Arguments:
        user_data = NewUserInput(required=True)

    user = Field(lambda: User, required=True)
    token = Field(lambda: Token, required=True)

    @staticmethod
    def mutate(root, info, user_data):
        email_check = UserModel.find_by_email(user_data.email)
        if email_check:
            raise Exception("email already exists")

        phone_number_check = UserModel.find_by_phone_number(user_data.phone_number)
        if phone_number_check:
            raise Exception("phone number already exists")

        user = UserModel(**user_data)
        user.password = generate_password_hash(user_data.password, method="sha256")

        user.save()
        return Signup(user=user, token=create_tokens(user))


class AddMember(Mutation):
    class Meta:
        name = "AddMember"
        description = "..."

    class Arguments:
        email = String(required=True)
        company_id = ID(required=True)

    ok = Boolean()

    @staticmethod
    def mutate(root, info, email, company_id):
        company = CompanyModel.find_by_id(company_id)
        if not company:
            raise Exception("company not found")

        user = User.find_by_email(email)
        if user:
            if user.company:
                raise Exception("user already belongs to a company")

            msg = f"We would like you to join our company '{company.name}'.\n" \
                  f"Please accept thought this link </>"

            send_email(email, msg)

            # TODO send invitation
            return AddMember(ok=True)

        # TODO create a url for sign up
        msg = f"We would like you to join our company '{company.name}'.\n" \
              f"Please sign up to this link </>"

        send_email(email, msg)

        return AddMember(ok=True)
