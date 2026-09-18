from fastapi import FastAPI , Depends , HTTPException
from sqlalchemy.orm import Session
from database import engine , Base , get_db
from models import User
from schemas import UserCreate , UserResponse , UserLogin
from security import password_hash

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Hello"}

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
            return {"message" : "login"}
        else :
            raise HTTPException(status_code=400 , detail= "Invalid email or password")
    raise HTTPException(status_code=400 , detail= "Invalid email or password")
        