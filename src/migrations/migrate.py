import mysql.connector
import os

def connect_to_database():
    """Connect to the MySQL database."""
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password="",
        database="lifeontrack-dev"
    )

def run_migrations():
    """Run SQL migrations to create necessary tables."""
    migration_script_path = os.path.join(os.path.dirname(__file__), "migrations.sql")

    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        with open(migration_script_path, "r") as file:
            sql_commands = file.read().split(";")

        for command in sql_commands:
            command = command.strip()
            if command:
                print(f"Executing: {command}")
                cursor.execute(command)
        
        connection.commit()
        print("Migrations applied sucessfully.")

    except mysql.connector.Error as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    run_migrations()