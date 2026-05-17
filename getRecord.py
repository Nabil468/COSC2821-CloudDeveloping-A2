import boto3
import json

dynamodb = boto3.client('dynamodb', region_name='us-east-1')

def lambda_handler(event, context):
    try:
        # Step 1: Validate input (400 Bad Request)
        if not isinstance(event, dict):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid input format — must be a JSON object.'})
            }

        # If student_name or course_year is provided, both must be present
        if ("student_name" in event and "course_year" not in event) or \
           ("course_year" in event and "student_name" not in event):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Both student_name and course_year must be provided together.'})
            }

        # Step 2: Run the correct query or scan
        if "student_name" in event and "course_year" in event:
            response = dynamodb.query(
                TableName='Course_Registration',
                IndexName='studentname-year-index',
                KeyConditionExpression='student_name = :name AND course_year = :year',
                ExpressionAttributeValues={
                    ':name': {'S': event['student_name']},
                    ':year': {'S': event['course_year']}
                }
            )
        else:
            response = dynamodb.scan(TableName='Course_Registration')

        # Step 3: Return 404 if no records found
        if not response.get('Items'):
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'No records found for the given criteria.'})
            }

        # Step 4: Return 200 with data
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])
        }

    except Exception as e:
        # Step 5: Return 500 for unexpected errors
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
