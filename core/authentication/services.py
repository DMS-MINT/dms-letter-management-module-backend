import uuid

from core.users.models import Member


def auth_user_get_jwt_secret_key(user: None) -> str:
    return str(user.jwt_key)


def auth_jwt_response_payload_handler(token, user=None, request=None, issued_at=None):
    return {
        "token": token,
    }


def auth_logout(user: Member) -> Member:
    user.jwt_key = uuid.uuid4()
    user.save(update_fields=["jwt_key"])

    return user
