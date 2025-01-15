import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="lifeontrack-dev",
    )

def find_user_by_auth0_id(auth0_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE auth0_id = %s", (auth0_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user


def insert_user(auth0_id, email, name):
    connection = get_db_connector()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO users (auth0_if, email, name) VALUES (%s, %s, %s)",
        (auth0_id, email, name),
    )
    connection.commit()
    user_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return {"id": user_id, "auth0_id": auth0_id, "email": email, "name": name}

def create_income(user_id, income_name, amount):
    connection = get_db_connection()
    cursor =  connection.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO incomes (user_id, income_name, amount) VALUES (%s, %s, %s)",
        (user_id, income_name, amount),
    )
    connection.commit()
    income_id=cursor.lastrowid
    cursor.close()
    connection.close()
    return {"id": income_id, "user_id": user_id, "income_name": income_name, "amount": amount}