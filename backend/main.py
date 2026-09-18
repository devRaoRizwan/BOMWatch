import jwt
from fastapi import FastAPI , Depends , HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from database import engine , Base , get_db
from models import User
from schemas import UserCreate , UserResponse , UserLogin
from security import password_hash , create_access_token , decode_access_token
from dependencies import get_current_user

app = FastAPI()

Base.metadata.create_all(bind=engine)



@app.get("/")
def home(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome {current_user.email}!"}

@app.post("/signup" , response_model=UserResponse)
def signup(user : UserCreate , db : Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user :
        raise HTTPException(status_code=400 , detail="User already exists")
    db_user = User(email = user.email , password = password_hash.hash(user.password))
    db.add(db_user)
    db.commit()
    return user

@app.post("/login")
def login(user : UserLogin , db : Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user :
        password_verified = password_hash.verify(user.password , existing_user.password)
        if password_verified:
            token = create_access_token(data={"sub" : str(existing_user.id)})
            return {"access_token" : token , "token_type" : "bearer"}
        else :
            raise HTTPException(status_code=400 , detail= "Invalid email or password")
    raise HTTPException(status_code=400 , detail= "Invalid email or password")
        