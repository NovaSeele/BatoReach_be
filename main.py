from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.base import api_router
from core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
# app.include_router(api_router, prefix="/api")


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.API_HOST,
                port=settings.API_PORT, reload=True)



# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from pydantic import BaseModel
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from passlib.context import CryptContext

# SECRET_KEY = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# db = {
#     "tim": {
#         "username": "tim",
#         "full_name": "Tim Ruscica",
#         "email": "tim@gmail.com",
#         "hashed_password": "$2b$12$HxWHkvMuL7WrZad6lcCfluNFj1/Zp63lvP5aUrKlSTYtoFzPXHOtu",
#         "disabled": False
#     }
# }


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     username: str or None = None


# class User(BaseModel):
#     username: str
#     email: str or None = None
#     full_name: str or None = None
#     disabled: bool or None = None


# class UserInDB(User):
#     hashed_password: str


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# app = FastAPI()


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)


# def get_user(db, username: str):
#     if username in db:
#         user_data = db[username]
#         return UserInDB(**user_data)


# def authenticate_user(db, username: str, password: str):
#     user = get_user(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False

#     return user


# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now() + expires_delta
#     else:
#         expire = datetime.now() + timedelta(minutes=15)

#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                          detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credential_exception

#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credential_exception

#     user = get_user(db, username=token_data.username)
#     if user is None:
#         raise credential_exception

#     return user


# async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")

#     return current_user


# @app.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}


# @app.get("/users/me/", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


# @app.get("/users/me/items")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": 1, "owner": current_user}]