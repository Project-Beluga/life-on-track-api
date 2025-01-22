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

def create_family(event, context):
    """
    Endpoint to create a family and send an invitation to a provided email.
    """
    try:
        body = json.loads(event['body'])
        owner_id = event['requestContext']['authorizer']['principalId']
        invited_email = body['invited_email']

        LOGGER.debug(f"Creating family with invitation to {invited_email}")

        connection = get_db_connection()
        cursor = connection.cursor()


        insert_family_query = """
            INSERT INTO families (owner_id, name)
            VALUES (%s, %s)
        """
        cursor.execute(insert_family_query, (owner_id, family_name))
        family_id = cursor.lastrowid

        insert_invitation_query = """
            INSERT INTO invitations (email, family_id, status)
            VALUES (%s, %s, 'pending')
        """
        cursor.execute(insert_invitation_query, (invited_email, family_id))
        connection.commit()

        LOGGER.info(f"Family created with ID {family_id} and invitation sent to {invited_email}")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Family created and invitation sent."})
        }
     
    except Exception as e:
        LOGGER.error(f"Error creating family: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()

def accept_invitation(event, context):
    """
    Endpoint to accept a family invitation and assign the user to the family.
    """
    try:
        body = json.loads(event['body'])
        invited_email = body['email']
        user_id = event['requestContext']['authorizer']['principalId']

        LOGGER.debug(f"User {user_id} accepting invitation for {invited_email}")

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        
        select_invitation_query = """
            SELECT family_id FROM invitations
            WHERE email = %s AND status = 'pending'
        """
        cursor.execute(select_invitation_query, (invited_email,))
        invitation = cursor.fetchone()

        if not invitation:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid or expired invitation."})
            }

        family_id = invitation['family_id']

        # Update user's family_id
        update_user_query = """
            UPDATE users
            SET family_id = %s
            WHERE id = %s
        """
        cursor.execute(update_user_query, (family_id, user_id))

        
        update_invitation_query = """
            UPDATE invitations
            SET status = 'accepted'
            WHERE email = %s
        """
        cursor.execute(update_invitation_query, (invited_email,))
        connection.commit()

        LOGGER.info(f"User {user_id} added to family {family_id}")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Invitation accepted and user added to the family."})
        }

    except Exception as e:
        LOGGER.error(f"Error accepting invitation: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()