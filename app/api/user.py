from models.user import User as UserModel
from models.company import Company as CompanyModel
from werkzeug.security import generate_password_hash
from .utils import DBInterface
from .auth import Token, create_tokens
from .role import Role
from graphene import ObjectType, Mutation, InputObjectType, String, Boolean, Field, ID, List
from common.utils import send_email


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

    @staticmethod
    def resolve_company(root, info):
        if root.company:
            return str(root.company.id)


class Login(ObjectType):
    class Meta:
        name = "Login"
        description = "..."

    user = Field(User)
    token = Field(Token)


class NewUserInput(InputObjectType):
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
        user_data = NewUserInput(required=True)

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
            return AddMember(ok=False)

        user = User.find_by_email(email)
        if user:
            if user.company:
                return AddMember(ok=False)

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
