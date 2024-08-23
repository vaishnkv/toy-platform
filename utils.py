
import json
from loguru import logger
from datetime import datetime



current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file_path = f"log/app_{current_time}.log"
# Configure the logger to write logs to the specified file
logger.add(log_file_path)



def read_json(file_path : str):
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data