import mysql.connector
import os

def connect_to_database():
    """Connect to the MySQL database."""
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "lifeontrack-dev")
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
        
        connection.comit()
        print("Migrations applied sucessfully.")

    except mysql.connector.Error as e:
        print(f"Error: {e}")
    
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    run_migrations()