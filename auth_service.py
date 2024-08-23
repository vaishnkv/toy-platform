import jwt
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from utils import read_json,logger
from flask_cors import CORS
import argparse
import os



app = Flask(__name__)

# Allow CORS only from a specific URL
# CORS(app, resources={r"/login": {"origins": "http://localhost:3001"}})
CORS(app)


try:
    VALID_USERS=read_json(os.getenv("USER_PASS_FILE"))
except FileNotFoundError:
    logger.info("User credentials file not found. Please set USER_PASS_FILE environment variable.")
    exit(1)




@app.route('/login', methods=['POST'])
def login():
    logger.info("Recieved a request in /login in Auth Service")
    username = request.json.get('username')
    password = request.json.get('password')
    # Validate username and password
    if username in VALID_USERS and VALID_USERS[username] == password:
        # Generate JWT token
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }
        token = jwt.encode(payload,os.getenv("SECRET_KEY"), algorithm='HS256')
        
        return jsonify({'token': token}),201
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/', methods=['GET'])
def root():
    return jsonify({'error': 'Invalid username or password'}), 200

if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(description="Script For Auth Service")
    # Add arguments
    parser.add_argument(
        "--port", type=int, required=False, help="Port to run",default=6300
    )
    args = parser.parse_args()
    logger.info(f"Starting Auth Service on port {args.port}")
    app.run(debug=True,port=args.port)
    