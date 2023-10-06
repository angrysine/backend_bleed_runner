from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv("./.env")

host = os.getenv("host")
port = os.getenv("port")
database = os.getenv("database")
user = os.getenv("user")
password = os.getenv("password")
aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")
aws_region = os.getenv("aws_region")
aws_bucket = os.getenv("aws_bucket")
aws_session_token = os.getenv("aws_session_token")
print("host: ", host, "port: ", port, "database: ",
      database, "user: ", user, "password: ", password)

conf = {
    'host': host,
    'port': port,
    'database': database,
    'user': user,
    'password': password,
    'aws_access_key_id': aws_access_key_id,
    'aws_secret_access_key': aws_secret_access_key,
    'aws_region': aws_region,
    'aws_bucket': aws_bucket,
    'aws_session_token': aws_session_token,
    "bucket": aws_bucket

}
engine = create_engine(
    f"postgresql://{user}:{password}@{host}:{port}/{database}")
# engine = create_engine("sqlite:///data.db")
