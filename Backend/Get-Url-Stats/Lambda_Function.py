import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("URLMappings")


def lambda_handler(event, context):

    # Get the short code from the URL path
    short_code = event.get("pathParameters", {}).get("shortCode")

    if not short_code:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Short code is required"
            })
        }

    # Look up the URL in DynamoDB
    response = table.get_item(
        Key={
            "shortCode": short_code
        }
    )

    # Check if the short URL exists
    if "Item" not in response:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "error": "Short URL not found"
            })
        }

    item = response["Item"]

    # Return URL statistics
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "shortCode": short_code,
            "originalUrl": item.get("originalUrl"),
            "clicks": item.get("clicks", 0)
        })
    }
