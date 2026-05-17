import json
import re

REQUIRED = ["course_name", "student_id", "student_email", "student_name", "course_year"]
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def lambda_handler(event, context):
    try:
        # 400 – bad input type
        if not isinstance(event, dict):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid input format — must be a JSON object"})
            }

        # 400 – missing required fields
        missing = [k for k in REQUIRED if k not in event or event[k] in (None, "", [])]
        if missing:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required fields", "fields": missing})
            }

        # 400 – format checks
        invalid = []
        if not EMAIL_RE.match(str(event["student_email"])):
            invalid.append("student_email")
        if not str(event["course_year"]).isdigit():
            invalid.append("course_year")
        if invalid:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid field format", "fields": invalid})
            }

        # 200 – echo back the clean payload
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Valid", "record": event})
        }

    except Exception as e:
        # 500 – unexpected errors
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
