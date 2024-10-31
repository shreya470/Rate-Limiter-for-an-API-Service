import requests
import json

# Set the base URL for your API
base_url = 'http://localhost:5000/api/v1/analytics'

# Define the submit_data function
def submit_data(auth_key, user_id, platform, content, timestamp):
    url = f'{base_url}/submit'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'user_id': user_id,
        'platform': platform,
        'content': content,
        'timestamp': timestamp
    }
    
    response = requests.post(url, headers=headers, params={'auth_key': auth_key}, json=payload)
    print('Submit Data Response:', response.status_code, response.json())

# Define the get_dashboard_data function
def get_dashboard_data(auth_key, user_id, platform=None, start_time=None, end_time=None):
    url = f'{base_url}/dashboard'
    params = {'user_id': user_id, 'auth_key': auth_key}
    
    if platform:
        params['platform'] = platform
    if start_time:
        params['start_time'] = start_time
    if end_time:
        params['end_time'] = end_time
    
    response = requests.get(url, params=params)
    print('Dashboard Data Response:', response.status_code, response.json())

# Example usage
if __name__ == '__main__':
    auth_key = 'auth_key_free'  # Replace with your actual auth key
    user_id = 'user123'  # Example user ID
    platform = 'Twitter'
    content = 'This is a test post'
    timestamp = '2024-10-31T10:00:00Z'  # Example timestamp in ISO 8601 format

    # Submit data to the API
    submit_data(auth_key, user_id, platform, content, timestamp)

    # Get dashboard data
    #get_dashboard_data(auth_key, user_id, platform, '2024-10-31T00:00:00Z', '2024-10-31T23:59:59Z')
