import json
import mysql.connector
from utils.json_logger import setup_logger


LOGGER = setup_logger()

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="lifeontrack-dev"
    )


def create(event, context):
    try:
        body = json.loads(event,['body'])
        user_id = event['requestContext']['authorizer']['principalId']
        income_name = body['income_name']
        amount = body['amount']
        currency = body['currency']

        LOGGER.debug(f"Creating income: {body}")

        connection = get_db_connection()
        cursor = connection.cursor()

        insert_query = """
            INSERT INTO incomes (user_id, income_name, amount, currency)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, income_name, amount, currency))
        connection.commit()

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Income added successfully"})
        }
    
    except Exception as e:
        LOGGER.error(f"Error adding income: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()

def get(event, context):
    try:
        user_id = event['requestContext']['authorizer']['principalId']

        LOGGER.debug(f"Fetching incomes for user_id: {user_id}")

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        select_query= """
            SELECT income_name, amount, currency
            FROM incomes
            WHERE user_id = %s
        """
        cursor.execute()
        incomes = cursor.fetchall()

        return {
            "statusCode": 200,
            "body": json.dumps({"data": incomes})
        }
    
    except Exception as e:
        LOGGER.error(f"Error fetching incomes: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
        
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()