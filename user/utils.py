import datetime
import jwt
from django.conf import settings

def generate_access_token(user):
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    exp_utc = now_utc + datetime.timedelta(days=30)
    access_token_payload = {
        "user_id": str(user.id),
        "exp": exp_utc,
        "iat": now_utc,
    }
    access_token = jwt.encode(
        access_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )
    return access_token

def generate_refresh_token(user):
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    exp_utc = now_utc + datetime.timedelta(days=30)
    refresh_token_payload = {
        "user_id": str(user.id),
        "exp": exp_utc,
        "iat": now_utc,
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )
    return refresh_token
