import json
import boto3
import uuid
from datetime import datetime, timezone

# AWS clients
ses = boto3.client("ses")
dynamodb = boto3.resource("dynamodb")

# Replace with your DynamoDB table name
TABLE_NAME = "reminders"
table = dynamodb.Table(TABLE_NAME)

# Replace with your verified SES sender email
SENDER_EMAIL = "nimblemayank@gmail.com"


def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        email = body["email"]
        message = body["message"]

        reminder_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        # 1️⃣ Save to DynamoDB
        table.put_item(
            Item={
                "reminderID": reminder_id,
                "email": email,
                "message": message,
                "remindAt": now,
                "status": "sent"
            }
        )

        # 2️⃣ Send Email Immediately
        ses.send_email(
            Source=SENDER_EMAIL,
            Destination={
                "ToAddresses": [email]
            },
            Message={
                "Subject": {"Data": "🚀 Cloud Reminder"},
                "Body": {
                    "Text": {
                        "Data": message
                    }
                }
            }
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Reminder sent successfully"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }
