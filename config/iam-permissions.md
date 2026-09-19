# IAM Permissions

The Lambda functions use IAM execution roles to access the required
AWS services without storing AWS credentials in the application code.

The permissions include:

- DynamoDB:
  - GetItem
  - PutItem
  - UpdateItem

- CloudWatch Logs:
  - CreateLogGroup
  - CreateLogStream
  - PutLogEvents

Access is granted through Lambda execution roles.
