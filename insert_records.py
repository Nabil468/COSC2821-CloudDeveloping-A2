import boto3, json

dynamodb = boto3.client('dynamodb', region_name='us-east-1')

with open('records.json') as f:
    records = json.load(f)

for item in records:
    response = dynamodb.put_item(TableName='Course_Registration', Item=item)
    print("Inserted:", item["student_id"]["S"])
