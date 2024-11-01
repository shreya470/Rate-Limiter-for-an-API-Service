from flask import Flask, request, jsonify
from rate_limiter import rate_limit_middleware, get_user_tier
import os
import uuid
import json
from model import db, SocialMediaPost 
from analytics import fetch_analytics 

#create base dic., app
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

#configure the database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  #initialize it with the Flask app


def load_config():
    with open('config.json') as config_file:
        return json.load(config_file)

#load config
config = load_config()

#access rate limits from the config
RATE_LIMITS = config.get("rate_limits", {})

def create_database():
    with app.app_context():
        db.create_all()

@app.route('/api/v1/analytics/submit', methods=['POST'])
@rate_limit_middleware
def submit_data():
    print("Request received at /api/v1/analytics/submit", flush=True)
    
    data = request.get_json()
    auth_key = request.args.get("auth_key") 

    if not auth_key:
        print("Authorization key is missing", flush=True)
        return jsonify({"error": "Authorization key is missing"}), 401
    
    user_id = data.get('user_id')  #get the user id from the JSON 
    platform = data.get('platform')
    content = data.get('content')
    timestamp = data.get('timestamp')

    if not user_id or not platform or not content or not timestamp:
        print("Missing required fields", flush=True)
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    analysis_id = str(uuid.uuid4())
    post = SocialMediaPost(id=analysis_id, user_id=user_id, platform=platform, content=content, timestamp=timestamp)
    try:
        db.session.add(post)
        db.session.commit()
        print(f"Data successfully stored with analysis_id: {analysis_id}", flush=True)
        return jsonify({"status": "success", "analysis_id": analysis_id}), 201
    except Exception as e:
        db.session.rollback()  #in case of error rollback the session 
        print(f"Error storing data: {e}", flush=True)
        return jsonify({"status": "error", "message": "Failed to store data"}), 500

@app.route('/api/v1/analytics/dashboard', methods=['GET'])
@rate_limit_middleware
def get_dashboard_data():

    user_id = request.args.get('user_id')
    platform = request.args.get('platform')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    analytics_data = fetch_analytics(user_id, platform, start_time, end_time)

    return jsonify(analytics_data), 200


if __name__ == '__main__':
    create_database()
    app.run(debug=True)
