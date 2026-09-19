Serverless URL Shortener

A fully serverless URL shortener built on AWS, using S3 + CloudFront for the frontend, API Gateway + Lambda for the backend logic, DynamoDB for storage and CloudWatch for monitoring.

Architecture

User Browser
     │
     ▼
CloudFront (URLShortnerCloudF)
     │
     ▼
S3 Static Website (serverless-url-shorterner-tony)
  - index.html / style.css / script.js
     │
     ▼ (API calls)
API Gateway (URLShortnerAPI)
     │
     ├── POST /  ──► CreateShortUrlFunction  ──► DynamoDB (put item)
     ├── GET  /{shortcode} ──► RedirectUrlFunction ──► DynamoDB (get + update clicks)
     └── GET  /stats/{shortcode} ──► GetUrlStatsFunction ──► DynamoDB (get item)

DynamoDB Table: URLMappings
  - shortCode (partition key)
  - originalUrl
  - clicks

CloudWatch
  - Alarms + Dashboard (URLShortnerDashboard) monitoring Lambda errors

Region: Europe (Spain) — eu-south-2

Components

1. Frontend (S3 + CloudFront)
S3 Bucket: serverless-url-shorterner-tony
Hosts index.html, style.css and script.js
index.html includes a placeholder long URL (e.g. anthonymuokem.com/very-long-url) that gets replaced by user input in the browser
CloudFront Distribution: URLShortnerCloudF
Default root object set to index.html
Serves the static site over HTTPS from the distribution domain name
Cache invalidations are run after frontend updates to reflect changes immediately

2. Database (DynamoDB)
Table: URLMappings
Attributes:
shortCode (String) — partition key
originalUrl (String) — the full/long URL(https://www.facebook.com)
clicks (Number) — click counter, incremented on each redirect

3. Backend (Lambda + API Gateway)
Lambda Function	Purpose	IAM Policy	DynamoDB Action
CreateShortUrlFunction	Generates a short code and stores the mapping	URLShortnerDynamoDBWrite	PutItem
RedirectUrlFunction	Looks up a short code and redirects to the original URL, incrementing clicks	URLShortenerDynamoDBRead / URLShortnerDynamoDBUpdate	GetItem, UpdateItem
GetUrlStatsFunction	Returns click statistics for a given short code as JSON	URLShortnerDynamoDBStatsRead	GetItem

All functions run on Python 3.13 and use scoped inline IAM policies limited to the URLMappings table ARN in the same region.

API Gateway: URLShortnerAPI
POST / → integrates with CreateShortUrlFunction
GET /{shortcode} → integrates with RedirectUrlFunction
GET /stats/{shortcode} → integrates with GetUrlStatsFunction
CORS enabled: GET, POST methods, Content-Type header, Access-Control-Allow-Origin: *
4. Monitoring (CloudWatch)
Metric alarm: GetUrlStatsFunction-Errors
Dashboard: URLShortnerDashboard with a widget tracking Lambda error metrics
Log groups:
/aws/lambda/CreateShortUrlFunction
/aws/lambda/GetUrlStatsFunction
/aws/lambda/RedirectUrlFunction
How It Works
User visits the site via the CloudFront distribution domain name.
User enters a long URL (e.g. facebook.com) into the input field.
script.js sends a POST request to the API Gateway invoke URL.
CreateShortUrlFunction generates a short code, writes {shortCode, originalUrl, clicks: 0} to DynamoDB, and returns the short URL.
Visiting {invoke-url}/{shortCode} triggers RedirectUrlFunction, which looks up the original URL, increments the clicks counter and redirects the browser.
Visiting {invoke-url}/stats/{shortCode} triggers GetUrlStatsFunction, which returns the current click count and original URL as JSON.

Setup Summary
I created an S3 bucket and upload index.html, style.css, script.js.
I created a CloudFront distribution pointing at the bucket, with index.html as the default root object.
I created a DynamoDB table (URLMappings) with shortCode as the partition key.
I created CreateShortUrlFunction (Python 3.13) with an inline IAM policy for PutItem, deploy, and test.
I created an API Gateway REST API, add a POST method integrated with CreateShortUrlFunction.
I created a RedirectUrlFunction with an inline policy for GetItem add a GET route in API Gateway integrated with it.
I had to enable CORS on the API (GET, POST, Content-Type header, Access-Control-Allow-Origin: *).
I Updated my script.js with the invoke URL and then invalidated the CloudFront cache to deploy frontend changes.
I added UpdateItem permission to RedirectUrlFunction to increment click counts on redirect.
I created a GetUrlStatsFunction with a GetItem policy and a GET /stats/{shortcode} route.
I set up CloudWatch alarms and a dashboard to monitor Lambda errors across all three functions.
Tech Stack
Frontend: HTML, CSS, JavaScript
Hosting/CDN: Amazon S3, Amazon CloudFront
API: Amazon API Gateway (REST API)
Compute: AWS Lambda (Python 3.13)
Database: Amazon DynamoDB
Monitoring: Amazon CloudWatch (Alarms, Dashboards, Logs)
IAM: Scoped inline policies per function (least-privilege access)


Built by Anthony Muokem as a hands-on AWS serverless architecture project.
