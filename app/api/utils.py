from graphene import (Interface, DateTime, ID)


class DBInterface(Interface):
    _id = ID()
    creation_date = DateTime()
    modified_date = DateTime()
