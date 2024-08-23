import jwt
import requests
from functools import wraps
from flask import Flask, request, jsonify
from datetime import datetime
import uuid
from loguru import logger
import json
from flask_cors import CORS
import argparse
import os 
from utils import read_json,logger



app = Flask(__name__)

CORS(app)


JOBS={}

try:
    VALID_USERS=read_json(os.getenv("USER_PASS_FILE"))
except FileNotFoundError:
    logger.info("User credentials file not found. Please set USER_PASS_FILE environment variable.")
    exit(1)


'''
Note:
    - Ideally , The Inside token_required function should hit one of the endpoint in auth_service.py. 
        Here we are doing this locally , will decouple in the future version.


'''



# utils function
def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        try:
            
            data = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=['HS256'])
            # Check if the token is valid and not expired
            if data['exp'] < datetime.utcnow().timestamp():
                return jsonify({'error': 'Token has expired'}), 401
            
            # Validate the username from the token
            username = data.get('username')
            if username not in VALID_USERS:
                return jsonify({'error': 'Invalid user'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return func(*args, **kwargs)
    
    return wrapper

# /submit_job endpoint for the job submission
@app.route('/job_submit', methods=['POST'])
@token_required
def middleware_submit_job():
    
    logger.info("Got a job submission request @ /job_submit within middleware")
    
    global middleware_url,core_service_url
    
    job_data = request.json

    job_id = str(uuid.uuid4()) # creating a unique job identifier
    
    JOBS[job_id]={
        "title": job_data["title"],
        "status": "In Progress",
        "created_at": str(datetime.now()),
        "completed_at": None
    }
    
    payload={
        "data":job_data["data"],
        "callback_url":f"{middleware_url}/job_callback/{job_id}"
    }
    

    # assert False
    
    response = requests.post(url=f'{core_service_url}/job_submit', json=json.dumps(payload))


    # assert False
    return jsonify(response.json()), response.status_code

# /job_callback endpoint
@app.route('/job_callback/<job_id>', methods=['POST'])
def job_callback(job_id):
    job_data = request.json
    if job_id in JOBS:
        JOBS[job_id]["status"]="Success" if job_data["status"]=="Success" else "Failure"
        JOBS[job_id]["completed_at"]=str(datetime.now())
        logger.info(f"Post process , got a value of : {job_data['modified_data']}")
        logger.info("Updated the DB from callback")
        logger.info(f"{JOBS}")
        return jsonify({"message":"Successfully updated"}),200
    else:
        return jsonify({'error': 'Job not found'}), 404
    
# /reset enpoint for reseting state 
@app.route('/reset', methods=['POST'])
@token_required
def middleware_reset():
    JOBS={}
    return jsonify({'message': 'Reset successful'}),200

# /list_jobs to get the list_of_jobs
@app.route('/list_jobs', methods=['GET'])
@token_required
def middleware_get_jobs():
    logger.info(f"Got a request to fetch the jobs")
    return jsonify({"jobs":list(JOBS.values())}),200

if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(description="Script For Auth Service")
    # Add arguments
    parser.add_argument(
        "--port", type=int, required=False, help="Port to run",default=6302
    )
    parser.add_argument(
        "--middleware_url", type=str, required=False, help="middleware_url",default="http://localhost:6302"
    )
    parser.add_argument(
        "--core_service_url", type=str, required=False, help="core_service_url",default="http://localhost:6301"
    )
    
    
    args = parser.parse_args()
    
    middleware_url=args.middleware_url
    core_service_url=args.core_service_url
    logger.info(f"Starting the middleware service on port {args.port}")
    app.run(port=args.port, debug=True)  