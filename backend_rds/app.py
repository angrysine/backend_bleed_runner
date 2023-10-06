from fastapi import FastAPI
import uvicorn
from routers.data import router as data_router
from routers.user import router as user_router
from routers.aws import router as aws_router
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "*"
]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
app.include_router(data_router)
app.include_router(user_router)
app.include_router(aws_router)

if __name__ == '__main__':
    uvicorn.run(app)
