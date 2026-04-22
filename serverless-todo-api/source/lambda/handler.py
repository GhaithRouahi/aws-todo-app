import json
import boto3
import uuid
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TODO_TABLE', 'TodoItems')
table = dynamodb.Table(table_name)

def _get_cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
    }

def create_todo(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        if 'task' not in body:
            return {
                'statusCode': 400,
                'headers': _get_cors_headers(),
                'body': json.dumps({'error': 'Task is required'})
            }

        todo_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        item = {
            'id': todo_id,
            'task': body['task'],
            'completed': False,
            'createdAt': timestamp,
            'updatedAt': timestamp
        }

        table.put_item(Item=item)

        return {
            'statusCode': 201,
            'headers': _get_cors_headers(),
            'body': json.dumps(item)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': _get_cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def read_todos(event, context):
    try:
        response = table.scan()
        return {
            'statusCode': 200,
            'headers': _get_cors_headers(),
            'body': json.dumps(response.get('Items', []))
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': _get_cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def read_todo(event, context):
    try:
        todo_id = event['pathParameters']['id']
        response = table.get_item(Key={'id': todo_id})
        
        if 'Item' in response:
            return {
                'statusCode': 200,
                'headers': _get_cors_headers(),
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'headers': _get_cors_headers(),
                'body': json.dumps({'error': 'Todo not found'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': _get_cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def update_todo(event, context):
    try:
        todo_id = event['pathParameters']['id']
        body = json.loads(event.get('body', '{}'))

        if 'task' not in body and 'completed' not in body:
            return {
                'statusCode': 400,
                'headers': _get_cors_headers(),
                'body': json.dumps({'error': 'Task or completed status is required'})
            }

        timestamp = datetime.utcnow().isoformat()
        
        update_expression = "SET updatedAt = :updatedAt"
        expression_attribute_values = {':updatedAt': timestamp}

        if 'task' in body:
            update_expression += ", task = :task"
            expression_attribute_values[':task'] = body['task']
        
        if 'completed' in body:
            update_expression += ", completed = :completed"
            expression_attribute_values[':completed'] = body['completed']

        response = table.update_item(
            Key={'id': todo_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )

        return {
            'statusCode': 200,
            'headers': _get_cors_headers(),
            'body': json.dumps(response['Attributes'])
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': _get_cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def delete_todo(event, context):
    try:
        todo_id = event['pathParameters']['id']
        
        table.delete_item(Key={'id': todo_id})
        
        return {
            'statusCode': 200,
            'headers': _get_cors_headers(),
            'body': json.dumps({'message': 'Todo deleted successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': _get_cors_headers(),
            'body': json.dumps({'error': str(e)})
        }
