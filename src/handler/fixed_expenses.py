import json
import mysql.connector
from utils.json_logger import setup_logger

LOGGER =  setup_logger()

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="lifeontrack-dev"
    )

def create(event, context):
    try:
        body = json.loads(event, ['body'])
        user_id = event['requestContext']['authorizer']['principalId']
        expense_name = body['income_name']
        amount = body['amount']
        currency = body['currency']
        
        LOGGER.debug(f"Creating fixed expense: {body}")


        connection = get_db_connection()
        cursor = connection.cursor()

        insert_query = """
            INSERT INTO expenses (user_id, expense_name, amount, currency)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(insert_query, (user_id, expense_name, amount, currency))
        connection.commit()

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Expense added successfully"})
        }

    except Exception as e:
        LOGGER.error(f"Error adding expense: {str(e)}")
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

        LOGGER.debug(f"Fetching expenses for user_id: {user_id}")

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        select_query= """
            SELECT expense_name, amount, currency
            FROM expenses
            WHERE user_id = %s
        """
        cursor.execute()
        expenses = cursor.fetchall()

        return {
            "statusCode": 200,
            "body": json.dumps({"data": expenses})
        }
    
    except Exception as e:
        LOGGER.error(f"Error fetching expenses: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
        
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()