from fastapi import APIRouter, UploadFile, Request
import boto3
import tempfile
from botocore.exceptions import NoCredentialsError
from fastapi.responses import JSONResponse
from routers.engine import conf
router = APIRouter()

session = boto3.Session(
    aws_access_key_id=conf["aws_access_key_id"].strip(),
    aws_secret_access_key=conf["aws_secret_access_key"],
    region_name=conf["aws_region"],
    aws_session_token=conf["aws_session_token"]
)
s3_client = session.client('s3')


@router.post("/uploadfile")
async def upload_parquet(file: UploadFile):

    try:
        # Crie um nome de arquivo temporário
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=".parquet")
        temp_file_name = temp_file.name
        # Leia o conteúdo do arquivo e salve-o no arquivo temporário
        with temp_file:
            temp_file.write(file.file.read())
        # Nome do arquivo no S3
        s3_file_name = 'reduced_data/' + file.filename
        bucket = conf["bucket"]
        # Faça upload do arquivo Parquet para o S3
        s3_client.upload_file(temp_file_name, bucket, s3_file_name)
        return JSONResponse(content={"message": "Arquivo Parquet enviado com sucesso para o S3!"})
    except NoCredentialsError:
        return JSONResponse(content={"message": "Credenciais AWS não encontradas. Verifique suas credenciais."}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao enviar o arquivo Parquet para o S3: {str(e)}"}, status_code=500)


@router.get("/listfiles")
async def list_files():
    try:
        bucket = conf["bucket"]
        files = s3_client.list_objects(Bucket=bucket)
        return JSONResponse(content={"message": files})
    except NoCredentialsError:
        return JSONResponse(content={"message": "Credenciais AWS não encontradas. Verifique suas credenciais."}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"message": f"Erro ao listar arquivos no S3: {str(e)}"}, status_code=500)


@router.get("/downloadfile")
async def download_file(request: Request):
    try:
        json = await request.json()
        file_name = json["file_name"]
        s3_client.download_file(
            conf["bucket"], f'reduced_data/{file_name}', file_name)

    except:
        return JSONResponse(content={"message": "Erro ao fazer download do arquivo"}, status_code=500)
