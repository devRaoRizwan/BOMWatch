from fastapi import FastAPI , Depends , HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
import jwt
from database import get_db
from models import User
from security import decode_access_token




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
        token : str = Depends(oauth2_scheme),
        db : Session = Depends(get_db)
    ):
    try:
        token_data = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = token_data.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401 , detail="Invalid token")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401 , detail="User not found")
    return user