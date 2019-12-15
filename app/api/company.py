from models.company import Company as CompanyModel
from models.role import EmbeddedRole
from models.user import User
from .utils import DBInterface
from .role import Role, StrictRoleInput
from graphene import ObjectType, Mutation, InputObjectType, String, Boolean, Field, List, InputField, ID
import smtplib


class CommonAttributes(object):
    name = String()
    email = String()
    phone_number = String()
    roles = List(Role)


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
            return NewCompany(ok=False)

        user = User.find_by_id(user_id)
        if user.company:
            return NewCompany(ok=False)

        owner_role = EmbeddedRole(name="owner", group=0, priority_level=0)

        company = CompanyModel(**company_data)
        company.roles.append(owner_role)
        company.save()

        user.role.append(owner_role)
        user.company = company
        user.save()

        return NewCompany(ok=True, company=company)


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
                  f"Please accept thought link http://127.0.0.1:5000/join"

            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.starttls()
            smtpObj.login('rizzmi.test@gmail.com', '123e456123e456')
            smtpObj.sendmail("justkiddingboat@gmail.com", email, msg)
            smtpObj.quit()

            # TODO send invitation
            return AddMember(ok=True)

        # TODO create a url for sign up
        msg = f"We would like you to join our company '{company.name}'.\n" \
              f"Please sign up to this link http://127.0.0.1:5000/signup"

        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login('rizzmi.test@gmail.com', '123e456123e456')
        smtpObj.sendmail("justkiddingboat@gmail.com", email, msg)
        smtpObj.quit()

        return AddMember(ok=True)

