from app import jwt
from datetime import timedelta
from graphene import ObjectType, String
from flask_jwt_extended import create_access_token, create_refresh_token


class Token(ObjectType):
    class Meta:
        name = "Token"
        description = "..."

    access = String(required=True)
    refresh = String(required=True)


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    result = {"role": [str(r._id) for r in user.role],
              "mode": "testing"}

    if user.company:
        result["company"] = str(user.company.id)

    return result


@jwt.user_identity_loader
def user_identity_lookup(user):
    return {"_id": str(user._id),
            # "email": user.email,
            "name": f"{user.first_name} {user.last_name}"}


def create_tokens(user, remember_me=False):
    access_token = create_access_token(identity=user, expires_delta=timedelta(minutes=10), fresh=False)
    if remember_me:
        refresh_token = create_refresh_token(identity=user, expires_delta=timedelta(days=30))
    else:
        refresh_token = create_refresh_token(identity=user, expires_delta=timedelta(days=1))

    return Token(access=access_token, refresh=refresh_token)


def create_fresh_token(user):
    access_token = create_access_token(identity=user, expires_delta=timedelta(minutes=1), fresh=True)
    return Token(access=access_token)


def refresh_access_token(user):
    new_token = create_access_token(identity=user, expires_delta=timedelta(minutes=10), fresh=False)
    return Token(access=new_token)

