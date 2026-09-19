import json
import boto3
import random
import string

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("URLMappings")


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def lambda_handler(event, context):

    # Get the URL sent by the user
    body = json.loads(event.get("body", "{}"))
    original_url = body.get("url")

    if not original_url:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "URL is required"
            })
        }

    # Generate a short code
    short_code = generate_short_code()

    # Save the URL in DynamoDB
    table.put_item(
        Item={
            "shortCode": short_code,
            "originalUrl": original_url,
            "clicks": 0
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "shortCode": short_code,
            "originalUrl": original_url
        })
    }
