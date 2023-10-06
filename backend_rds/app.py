from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.rds import Base, engine, metadata   
from routers import data_treatment
from models.treated import MaxData, MinData, MeanData, ModeData, StdData
from models.user import User

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    try: 
        print("Starting connection...")
        Base.metadata.create_all(bind=engine, checkfirst=True)
    except Exception as e:
        print("Error creating tables")
        raise e
    finally:
        print("Startup finished!")

app.include_router(data_treatment.router, 
                tags=["Data"]
            )



