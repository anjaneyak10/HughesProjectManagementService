import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', "my_precious")
    DATABASE_URI = os.getenv('DATABASE_URL',"postgresql://dhruvin:xAWgJcJgN3ggjktxM-oByA@hughesdb-7706.g8z.gcp-us-east1.cockroachlabs.cloud:26257/hughesservicedelivery")
