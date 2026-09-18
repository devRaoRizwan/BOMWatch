from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "1a4d752d457fd365b4181a1d50d7e4897b2483be77e19c1ba77498af7908f8d9"
ALGORITHM = "HS256"
password_hash = PasswordHash.recommended()

def create_access_token(data):
    data = data.copy()
    data["exp"] = datetime.now(timezone.utc) + timedelta(minutes=2)

    encoded_jwt = jwt.encode(
        payload=data,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def decode_access_token(token):
    decoded_jwt = jwt.decode(
        jwt=token,
        key=SECRET_KEY,
        algorithms=[ALGORITHM]
    )
    return decoded_jwt