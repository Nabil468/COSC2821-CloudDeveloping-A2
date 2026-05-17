import json
import re
import boto3

TABLE = "Course_Registration"
REGION = "us-east-1"
REQUIRED = ["course_name", "student_id", "student_email", "student_name", "course_year"]
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

dynamodb = boto3.client("dynamodb", region_name=REGION)

def lambda_handler(event, context):
    try:
        # 400: Basic validation
        if not isinstance(event, dict):
            return {"statusCode": 400,
                    "body": json.dumps({"error": "Invalid input format — must be a JSON object"})}

        missing = [k for k in REQUIRED if k not in event or event[k] in (None, "", [])]
        if missing:
            return {"statusCode": 400,
                    "body": json.dumps({"error": "Missing required fields", "fields": missing})}

        if not EMAIL_RE.match(str(event["student_email"])):
            return {"statusCode": 400,
                    "body": json.dumps({"error": "Invalid field format", "fields": ["student_email"]})}

        if not str(event["course_year"]).isdigit():
            return {"statusCode": 400,
                    "body": json.dumps({"error": "Invalid field format", "fields": ["course_year"]})}

        # Put item into DynamoDB
        dynamodb.put_item(
            TableName=TABLE,
            Item={
                "course_name":   {"S": str(event["course_name"])},
                "student_id":    {"S": str(event["student_id"])},
                "student_email": {"S": str(event["student_email"])},
                "student_name":  {"S": str(event["student_name"])},
                "course_year":   {"S": str(event["course_year"])},
            }
        )

        # 200: Success
        return {"statusCode": 200,
                "body": json.dumps({"message": "Record saved successfully"})}

    except Exception as e:
        # 500: Unexpected AWS/other error
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
