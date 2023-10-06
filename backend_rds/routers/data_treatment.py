from fastapi import APIRouter, HTTPException, UploadFile, Request
from sqlalchemy import insert, select,text
from models.treated import class_handler
from pathlib import Path
import pandas as pd

from config import s3, rds

router = APIRouter()

@router.post("/s3_sent_files")
async def s3_post(file: UploadFile):
    try:
        """
        Upload de arquivo para o S3
        """
        #! Teste de presigned URL
        response = s3.generate_presigned_post(file.filename)
        if response is not None and Path(file.filename).suffix == '.parquet':
            s3.teste_client.upload_fileobj(file.file, s3.bucket_name, 'raw/' + file.filename)
        # if Path(file.filename).suffix == '.parquet':
        #     s3.client.upload_fileobj(file.file, s3.bucket_name, 'raw/' + file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error generating presigned URL, {e}')
    return {'message': 'success'}

# @router.get("/rds_get_data")
# async def rds_get_data():
#     try:
#         """
#         Consulta de dados no RDS
#         """
#         response = rds.teste_client.execute('SELECT * FROM raw_data')
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f'Error getting data from RDS, {e}')
#     return response

@router.post("/add_data", tags=["Data"])
async def add_data(request: Request):
    try:
        json_list = await request.json()
        parquet_list = json_list["data"]
        table_name = json_list["table_name"]
        print(table_name)
        with rds.conn.begin():
            rds.conn.execute(insert(class_handler[table_name]), parquet_list)

        return {"message": "Data added successfully"}
    except Exception as e:
        print(e)
        return {"message": str(e)}
    
@router.get("/get_data", tags=["data"])
async def get_data(request: Request):
    try:
        json_list = await request.json()
        table_name = json_list["table_name"]
        with rds.engine.begin():
            query = select(class_handler[table_name])
            result = rds.conn.execute(query)
            data = result.fetchall()
            df = pd.DataFrame(data)
            df.columns = result.keys()
            return df.to_dict(orient="records")
    except Exception as e:
        print(e)
        return {"message": str(e)}
    

@router.get("/failures_time", tags=["data"])
async def failures_time(request: Request):
    try:
        json_list = await request.json()
        table_name = json_list["table_name"]
        with rds.engine.begin() as conn:
            # query = text(
            #     "SELECT date,time_to_failure ,aircraftsernum_1 FROM aircraft_data;")
            query = select(class_handler[table_name].date,class_handler[table_name].time_to_failure,class_handler[table_name].aircraftsernum_1)
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
        with rds.engine.begin():
            # query = text(
            #     "SELECT date,time_to_failure ,aircraftsernum_1 FROM aircraft_data;")
            query = select(class_handler[table_name].cumulative_duration).filter(class_handler[table_name].aircraftsernum_1 == aircraftsernum_1).order_by(class_handler[table_name].cumulative_duration.desc()).limit(1)
            #query = text(f"SELECT cumulative_duration FROM aircraft_data WHERE aircraftsernum_1 = {aircraftsernum_1} ORDER BY cumulative_duration DESC LIMIT 1;")
            result = rds.conn.execute(query)
            data = result.fetchall()

        return data[0][0]

    except Exception as e:
        print(e)
        return {"message": str(e)}
