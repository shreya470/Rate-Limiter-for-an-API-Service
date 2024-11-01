# Rate Limiter for an API Service

This is a Flask-based API service that allows users to submit social media posts and retrieve analytics. The API includes a rate-limiting feature to manage requests based on user tiers.

## Table of Contents
- [Rate Limiter for an API Service](#rate-limiter-for-an-api-service)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Rate Limiting Approach](#rate-limiting-approach)
  - [Configuration](#configuration)
  - [Prerequisites](#prerequisites)
  - [Running the Service](#running-the-service)
  - [Testing the API](#testing-the-api)
  - [Test Cases](#test-cases)
  - [Conclusion](#conclusion)
  - [Documentation\*\*](#documentation)

## Overview

The Rate limiter allows users to submit posts and get insights such as sentiment analysis and the most frequently used hashtags, it enforces different request limits based on user tiers.

## Rate Limiting Approach

The API uses a sliding window mechanism for rate limiting, which tracks the timestamps of requests made by users:

- **Per Minute Limit**: Users can make a certain number of requests within a minute.
- **Per Hour Limit**: Users can make a certain number of requests within an hour.
- Users are categorized into tiers (e.g., free, standard, premium) which have different limits defined in the `config.json` file.

When a user exceeds their limit, the API responds with a `429 Too Many Requests` status code, and the response includes the time to wait before the user can retry the request.

## Configuration

To configure the API, you need a `config.json` file with the following structure:

```json
{
    "rate_limits": {
      "free": {
        "per_minute": 10,
        "per_hour": 100
      },
      "standard": {
        "per_minute": 50,
        "per_hour": 500
      },
      "premium": {
        "per_minute": 200,
        "per_hour": 2000
      }
    },
    "user_tiers": {
      "auth_key_free": "free",
      "auth_key_standard": "standard",
      "auth_key_premium": "premium"
    }
  }
```
## Prerequisites
Before you begin, ensure you have the following installed on your system
- Python (version 3.6 or later)
- pip (Python package installer)

You will need to install the following dependencies:

``` bash
pip install Flask Flask-SQLAlchemy textblob requests nltk
```
## Running the Service
Follow these steps to run the service:

**Clone the Repository:**
 Clone your project repository to your local machine.

```bash

git clone https://github.com/shreya470/Rate-Limiter-for-an-API-Service
cd your-repo
```

**Configure the Database:** Ensure the database is set up and configured in your Flask application.

**Load Configuration:** Create a config.json file as described in the configuration section.

**Run the Application:** Start the Flask application using the following command:

```bash
python app.py
```
**Access the API:** Use the API client provided in api_client.py to interact with the API.

## Testing the API
Use the api_client.py script provided in the project to call the API endpoints. You can modify the script to test different functionalities like submitting data and fetching dashboard data.

Submit Data: To submit data to your API, run the api_client.py script. Make sure to configure the auth_key, user_id, platform, content, and timestamp variables as needed in the script.

Fetch Dashboard Data: Similarly, you can modify and run api_client.py to fetch dashboard data based on user ID and other parameters.

```bash
python api_client.py
```
## Test Cases

- **Test Case 1:** Successful Data Submission
**Description:** Ensure that a user can successfully submit a post with valid data.
**Input:** 
```json
{
  "user_id": "user_123",
  "platform": "Twitter",
  "content": "Sample content",
  "timestamp": "2024-10-32T12:00:00Z"
}

```
**Expected Outcome:** 
```json
{
    "analysis_id": "ed28bd59-69b4-4723-aa8e-9aac32374efe",
    "status": "success"
}
```


- **Test Case 2:** Missing Required Fields
**Description:** Test the response when required fields are missing from the submission.
Input:
```json
{
  "user_id": "user_123",
  "content": "Sample content",
  "timestamp": "2024-10-32T12:00:00Z"
}
```

**Expected Outcome:**
```json
{
    "message": "Missing required fields",
    "status": "error"
}
```

- **Test Case 3:** Rate Limiting
**Description:** Validate that the rate limiter restricts requests based on user tier.


**Input:** Send requests that exceed the allowed limit for that tier.(auth_key_free)
```json
{
  "user_id": "user_123",
  "platform": "Twitter",
  "content": "Sample content",
  "timestamp": "2024-10-32T12:00:00Z"
}

```

**Expected Outcome:**
```json
{
    "error": "Exceeded per-minute rate limit",
    "retry_after": 49.42471098899841,
    "unit": "seconds"
}
```

- **Test Case 4:** Dashboard Data Retrieval
**Description:** Ensure that users can retrieve analytics data correctly.

**Input:** 
user_id: "user1"
auth_key: "auth_key_free"
platform: "Twitter"
start_time: "2024-10-26T00:00:00"
end_time: "2024-10-27T23:59:59"


**Expected Outcome:**
```json
{
    "mentions_count": 3,
    "sentiment_score": 0.0893939393939394,
    "top_hashtags": []
}
```

## Conclusion
In the conclusion section, summarize the key points of your API and its functionality:

This Social Media Analytics API provides a robust solution for tracking and analyzing social media posts while ensuring fair usage through an effective rate-limiting strategy. With support for different user tiers and flexible data submission and retrieval capabilities, the API is designed to facilitate insightful analytics for users.

## Documentation**
  Pfb the link to the documentation here
  https://docs.google.com/document/d/1sozsoiYAAApWfHJP0eEg18IAuXXB9irGY0zKCBaEpnA/edit?addon_store&tab=t.0
