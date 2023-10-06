from fastapi import APIRouter, Request
from routers.engine import engine
from models.data import class_handler
from sqlalchemy import text, insert, select
import pandas as pd
from auth.token_creator import decode_access_token
import matplotlib.pyplot as plt
import base64

from routers.engine import conf
# dependencies=[Depends(decode_access_token)]
router = APIRouter()


@router.post("/add_data", tags=["data"])
async def add_data(request: Request):
    try:
        json_list = await request.json()
        parquet_list = json_list["data"]
        table_name = json_list["table_name"]
        with engine.begin() as conn:

            conn.execute(insert(class_handler[table_name]), parquet_list)

        return {"message": "Data added successfully"}
    except Exception as e:
        print(e)
        return {"message": str(e)}


@router.get("/get_data", tags=["data"])
async def get_data(request: Request):
    try:
        json_list = await request.json()
        table_name = json_list["table_name"]
        with engine.begin() as conn:
            query = select(class_handler[table_name])
            result = conn.execute(query)
            data = result.fetchall()
            df = pd.DataFrame(data)
            df.columns = result.keys()
            return df.to_dict(orient="records")
    except Exception as e:
        print(e)
        return {"message": str(e)}


@router.get("/graph", tags=["data"])
async def graph(request: Request):
    try:
        json_list = await request.json()
        table_name = json_list["table_name"]
        with engine.begin() as conn:
            # redo this with select
            table = class_handler[table_name]
            query = select().with_only_columns(
                [table.date, table.time_to_failure, table.aircraftSerNum_1])
            result = conn.execute(query)
            data = result.fetchall()
            df = pd.DataFrame(data)
            df["date"] = pd.to_datetime(df["date"])
            df["month"] = df["date"].dt.month
            df = df[df["time_to_failure"] == 0]
            df[["month", "time_to_failure"]].groupby("month").count().plot(
                title="Number of failures per month", kind="bar", xlabel="Month", ylabel="Number of failures", rot=0)
            plt.savefig("graph.png")
            with open("graph.png", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            return {"message": encoded_string.decode("utf-8")}

    except Exception as e:
        print(e)
        return {"message": str(e)}


@router.get("/failures_time", tags=["data"])
async def failures_time(request: Request):
    try:
        json_list = await request.json()
        table_name = json_list["table_name"]
        with engine.begin() as conn:
            # query = text(
            #     "SELECT date,time_to_failure ,aircraftsernum_1 FROM aircraft_data;")
            query = select(class_handler[table_name]).with_only_columns(
                [class_handler[table_name].date, class_handler[table_name].time_to_failure, class_handler[table_name].aircraftSerNum_1])
            result = conn.execute(query)
            data = result.fetchall()

        df = pd.DataFrame(data)

        df["date"] = pd.to_datetime(df["date"])
        max_values = df.groupby("aircraftsernum_1")['date'].idxmax()

        df2 = df.loc[max_values, ['time_to_failure', "aircraftsernum_1"]]
        del df, max_values
        return df2.to_dict(orient="records")

    except Exception as e:
        print(e)
        return {"message": str(e)}


@router.get("/cumulative_time", tags=["data"])
async def cumlative_time(request: Request):
    try:
        json_list = await request.json()
        table_name = json_list["table_name"]
        aircraftsernum_1 = json_list["aircraftsernum_1"]
        with engine.begin() as conn:
            # query = text(
            #     "SELECT date,time_to_failure ,aircraftsernum_1 FROM aircraft_data;")
            query = select(class_handler[table_name]).filter(class_handler[table_name].aircraftsernum_1 == aircraftsernum_1).with_only_columns(
                [class_handler[table_name].cumulative_duration]).order_by(class_handler[table_name].cumulative_duration.desc()).limit(1)
            result = conn.execute(query)
            data = result.fetchall()

        return data[0]

    except Exception as e:
        print(e)
        return {"message": str(e)}
