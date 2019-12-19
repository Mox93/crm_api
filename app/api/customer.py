from models.customer import Customer as CustomerModel
from models.company import Company as CompanyModel
from models.campaign import Campaign as CampaignModel
from .utils import DBInterface
from graphene import ObjectType, Mutation, InputObjectType, String, Field, ID


class CommonAttributes(object):
    first_name = String()
    last_name = String()
    email = String()
    phone_number = String()
    company = ID()
    source = ID()


class CustomerInterface(CommonAttributes, DBInterface):
    pass


class Customer(ObjectType):
    class Meta:
        name = "Customer"
        description = "..."
        interfaces = (CustomerInterface,)


class StrictCustomerInput(InputObjectType):
    first_name = String(required=True)
    last_name = String(required=True)
    email = String(required=True)
    phone_number = String(required=True)


class AddCustomer(Mutation):
    class Meta:
        name = "AddCustomer"
        description = "..."

    class Arguments:
        campaign_id = ID(required=True)
        customer_data = StrictCustomerInput(required=True)

    customer = Field(lambda: Customer)

    @staticmethod
    def mutate(root, info, campaign_id, customer_data):
        campaign = CampaignModel.find_by_id(campaign_id)
        if not campaign:
            raise Exception("Campaign not found!")

        company = campaign.company.fetch()
        if not company:
            raise Exception("Company not found!")

        customer = CustomerModel(**customer_data, source=campaign, company=company)
        customer.save()

        return AddCustomer(customer=customer)

