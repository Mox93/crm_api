from models.product import Product as ProductModel
from models.company import Company as CompanyModel
from models.campaign import Campaign as CampaignModel
from .utils import DBInterface
from graphene import ObjectType, Mutation, InputObjectType, String, Field, ID


class CommonAttributes(object):
    name = String()
    description = String()
    product = ID()
    platform = String()
    company = ID()


class CampaignInterface(CommonAttributes, DBInterface):
    pass


class Campaign(ObjectType):
    class Meta:
        name = "Campaign"
        description = "..."
        interfaces = (CampaignInterface,)


class StrictCampaignInput(InputObjectType):
    name = String(required=True)
    description = String()
    platform = String()


class NewCampaign(Mutation):
    class Meta:
        name = "NewCampaign"
        description = "..."

    class Arguments:
        company_id = ID(required=True)
        product_id = ID(required=True)
        campaign_data = StrictCampaignInput(required=True)

    campaign = Field(lambda: Campaign)

    @staticmethod
    def mutate(root, info, company_id, product_id, campaign_data):
        company = CompanyModel.find_by_id(company_id)
        if not company:
            raise Exception("Company not found!")

        product = ProductModel.find_by_id(product_id)
        if not product:
            raise Exception("Product not found!")

        campaign = CampaignModel(**campaign_data, product=product, company=company)
        campaign.save()

        return NewCampaign(campaign=campaign)

