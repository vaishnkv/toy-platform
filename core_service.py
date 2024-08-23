from flask import Flask, request, jsonify
from queue import Queue
from utils import logger
import threading
import json
import time
import requests
import argparse


app = Flask(__name__)
task_queue = Queue()




@app.route('/job_submit', methods=['POST'])
def job_submit():
    data=json.loads(request.json)
    if data:
        task_queue.put(data)
        logger.info("Job submitted in the Queue.")
        return jsonify({"status": "Task added to the queue"}), 202
    else:
        return jsonify({"error": "No data provided"}), 400

@app.route('/queue_size', methods=['GET'])
def queue_size():
    return jsonify({"queue_size": task_queue.qsize()}), 200


# Worker thread that continuously processes tasks from the queue
def worker():
    while True:
        task = task_queue.get()
        if task is None:
            break  # Exit the worker if a None task is received (optional)
        run(task)
        task_queue.task_done()

# The core-business logic resides here
def transformation(data):
    time.sleep(20)
    return "".join(list(reversed(data)))
    
# wrapper around tranformation function
def run(input_data):
    data=input_data.get("data")
    result=transformation(data)
    payload={"modified_data":result,"status":"Success"}
    callback_url = input_data.get("callback_url",None)
    if callback_url:
        json_payload = json.dumps(payload)
        headers = {'Content-Type': 'application/json'}
        response=requests.post(url=callback_url, data=json_payload, headers=headers)
        logger.info(f"response.status_code: {response.status_code} response.text: {response.text}")
        if response.status_code == 200:
            logger.debug(f'POST request successful {callback_url}')
        else:
            logger.debug(f'POST request failed with status code {response.status_code}')
    else:
        logger.info("No callback URL provided.")
        

# Start the worker thread
worker_thread = threading.Thread(target=worker)
worker_thread.daemon = True  # Daemonize the thread to exit when the main program exits
worker_thread.start() 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script For the Core Service")
    # Add arguments
    parser.add_argument(
        "--port", type=int, required=False, help="Port to run",default=6301
    )
    args = parser.parse_args()
    logger.info(f"Starting the Core Service on port {args.port}")
    app.run(debug=True,port=args.port)

# npx create-react-app my-login 