from .models import CustomUser
from flat_tokens.models import Token


def generate_token(username)->Token:
    user = CustomUser.objects.filter(username=username).first()
    Token.clear_expired_tokens()
    token = Token.objects.create(user=user)
    return token