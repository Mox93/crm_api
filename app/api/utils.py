from graphene import (Interface, DateTime, ID)


class DBInterface(Interface):
    _id = ID(required=True)
    creation_date = DateTime(required=True)
    modified_date = DateTime(required=True)
