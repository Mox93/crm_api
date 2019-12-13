from models.user import User as UserModel
from graphene import ObjectType, Mutation, InputObjectType, String, Boolean, Field, ID, DateTime
from werkzeug.security import generate_password_hash


class User(ObjectType):
    class Meta:
        name = "User"
        description = "..."

    _id = ID()
    creation_date = DateTime()
    modified_date = DateTime()

    first_name = String()
    last_name = String()
    email = String()
    phone_number = String()


class Signup(Mutation):
    class Meta:
        name = "Signup"
        description = "..."

    class Arguments:
        first_name = String(required=True)
        last_name = String(required=True)
        email = String(required=True)
        phone_number = String(required=True)
        password = String(required=True)

    ok = Boolean()
    user = Field(User)

    @staticmethod
    def mutate(root, info, first_name, last_name, email, phone_number, password):
        email_check = UserModel.find_by_email(email)
        if email_check:
            return Signup(ok=False)
        phone_number_check = UserModel.find_by_phone_number(phone_number)
        if phone_number_check:
            return Signup(ok=False)

        hash_password = generate_password_hash(password, method="sha256")

        user = UserModel(first_name=first_name,
                         last_name=last_name,
                         email=email,
                         phone_number=phone_number,
                         password=hash_password)

        user.save()
        return Signup(ok=True, user=user)

