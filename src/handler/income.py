import json
import boto3

dynamodb = boto3.resource('dynamodb')
table =  dynamodb.Table('Incomes')

def create(event, context):
    try:
        body = json.loads(event,['body'])
        user_id = event['requestContext']['authorizer']['principalId']
        income_name = body['income_name']
        amount = body['amount']
        currency = body['currency']

        table.put_item(
            Item={
                'user_id': user_id
                'income_name': income_name,
                'amount': amount,
                'currency': currency
            }
        )

        return {
            "statusCode":200
            "body": json.dumps({"message": "Income added successfully!"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

def get(event, context):
    try:
        user_id = event['requestContext']['authorizer']['principalId']

        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id)
        )
        return {
            "statusCode": 200,
            "body": json.dumps({"data": response['Items']})
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }