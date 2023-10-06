from fastapi import APIRouter, Request, HTTPException
from models.user import User
from sqlalchemy import select, insert, update
from routers.engine import engine
from auth.token_creator import create_access_token
router = APIRouter()


@router.post("/add_user", tags=["user"])
async def create_user(request: Request):
    try:
        data = await request.json()
        # salt = bcrypt.gensalt()
        #  bcrypt.hashpw(
        #         data["password"].encode("utf-8"), salt)
        with engine.begin() as conn:
            #check if user exists
            stm = select(User).where(User.username == data["username"])
            result = conn.execute(stm).fetchone()
            if result:
                raise Exception("User already exists")
            
        with engine.begin() as conn:
            conn.execute(insert(User), {
                         "username": data["username"], "password": data["password"], "date": "", "user_secret": ""})
        return {"message": "user created"}

    except Exception as e:
        print(e)
        return HTTPException(status_code=400, detail=str(e))


@router.post("/login", tags=["user"])
async def login(request: Request):

    try:
        data = await request.json()
        with engine.begin() as conn:
            password = data["password"]
            username = data["username"]
            stm = select(User).where(User.username == username)
            result = conn.execute(stm).fetchone()

            # Encode the password as bytes
            password_bytes = password.encode("utf-8")

            # if bcrypt.checkpw(password_bytes, result.password):

            token, secret = create_access_token(
                {"username": username, "password": password})
            stm = update(User).where(User.username ==
                                     username).values(user_secret=secret)
            conn.execute(stm)
            return {"token": token}
        # else:
        #     raise Exception("Invalid user or password")
    except Exception as e:
        return {"error": str(e)}
