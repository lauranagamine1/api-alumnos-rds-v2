import boto3
import pymysql
import os
import json

def lambda_handler(event, context):
    secret_id = os.environ['DB_SECRET_ARN']
    database = os.environ['DB_NAME']

    sm = boto3.client('secretsmanager')
    response = sm.get_secret_value(SecretId=secret_id)
    secret = json.loads(response['SecretString'])

    host = secret['host']
    user = secret['username']
    password = secret['password']

    connection = None  

    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=database,
            connect_timeout=5
        )

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM alumnos;")
            results = cursor.fetchall()

        return {
            "statusCode": 200,
            "body": json.dumps(results, default=str)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }

    finally:
        if connection:  
            connection.close()