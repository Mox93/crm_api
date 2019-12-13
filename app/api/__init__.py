from graphene import Schema, ObjectType, List, Field, ID, String, Int, Boolean
from models.user import User as UserModel


class QueryType(ObjectType):
    class Meta:
        name = "Query"
        description = "..."

    seen = []

    greeting = String(name=String(required=True))

    @staticmethod
    def resolve_greeting(root, info, name):
        if name in QueryType.seen:
            return f"Welcome back {name}!"
        QueryType.seen.append(name)
        return f"Welcome {name}!"


class MutationType(ObjectType):
    class Meta:
        name = "Mutation"
        description = "..."


schema = Schema(query=QueryType)  # , mutation=MutationType
