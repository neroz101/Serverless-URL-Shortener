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

    # Look up the short code in DynamoDB
    response = table.get_item(
        Key={
            "shortCode": short_code
        }
    )

    # Check if the short code exists
    if "Item" not in response:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "error": "Short URL not found"
            })
        }

    original_url = response["Item"]["originalUrl"]

    # Redirect the user
    return {
        "statusCode": 302,
        "headers": {
            "Location": original_url
        },
        "body": ""
    }
