from flask import request, jsonify
from datetime import datetime, timedelta
import json
import time

with open('config.json') as config_file:
    config = json.load(config_file)

#get the rate limits for each tier
RATE_LIMITS = config["rate_limits"]

#classify user data based on auth keys
USER_TIERS = config["user_tiers"]

#track requests per user
request_records = {}

def get_user_tier(auth_key):
    #get the user tier on the basis of auth key
    return USER_TIERS.get(auth_key, "free")  

def is_rate_limited(auth_key):
    #check if a user is rate-limited
    tier = get_user_tier(auth_key)
    limits = RATE_LIMITS[tier]
    user_requests = request_records.setdefault(auth_key, {"minute": [], "hour": []})
    

    current_time = time.time()
    
    #clear out expired requests ie older than 1 minute or 1 hour
    user_requests["minute"] = [t for t in user_requests["minute"] if current_time - t < 60]
    user_requests["hour"] = [t for t in user_requests["hour"] if current_time - t < 3600]
    
    print(f"Requests in last minute for {auth_key}: {len(user_requests['minute'])+1}")
    print(f"Requests in last hour for {auth_key}: {len(user_requests['hour'])+1}")
    print(f"Current request records: {request_records}", flush=True)  # Debugging line

    
    #check the rate limits
    if len(user_requests["minute"]) >= limits["per_minute"]:
        wait_time = 60 - (current_time - user_requests["minute"][0])
        return True, "Exceeded per-minute rate limit", wait_time

    if len(user_requests["hour"]) >= limits["per_hour"]:
        wait_time = 3600 - (current_time - user_requests["hour"][0])
        return True, "Exceeded per-hour rate limit", wait_time
   
    
    #find out the current request time
    user_requests["minute"].append(current_time)
    user_requests["hour"].append(current_time)
    
    return False, "Within rate limits", 0

def rate_limit_middleware(func):
    #rate limiting middleware to apply on routes
    def wrapped_function(*args, **kwargs):
        auth_key = request.args.get("auth_key")
        print(f"Extracted auth key: {auth_key}")  # Add this line for debugging
  
        if not auth_key:
            return jsonify({"error": "Missing auth key"}), 401
        
        print(f"Received auth key: {auth_key}", flush=True)

        is_limited, message, wait_time = is_rate_limited(auth_key)
        if is_limited:
            return (
                jsonify({"error": message, "retry_after": wait_time, "unit": "seconds"}),
                429,
                {"Retry-After": str(int(wait_time))} 
            )        
        return func(*args, **kwargs)
    
    wrapped_function.__name__ = func.__name__  #ensure that the name is unique
    return wrapped_function
