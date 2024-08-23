

# Activate the virtual environment
echo "Activating the virtual environment..."
source testenv/bin/activate

# Set the environment variables
echo "Setting environment variables..."

export SECRET_KEY=KEY
export AUTH_SERVICE_PORT=6300 MIDDLEWARE_PORT=6302 CORE_SERVICE_PORT=6301
export CORE_SERVICE_URL="http://localhost:6301" MIDDLEWARE_URL="http://localhost:6302"
export USER_PASS_FILE="user_pass_lookup.json"
# We are fixing the AUTH_SERVICE_URL to be "http://localhost:6300"



# Start the Flask servers in the background and capture their PIDs
echo "Starting Flask servers..."

python3 auth_service.py &
PID1=$!
python3 core_service.py &
PID2=$!
python3 middleware.py &
PID3=$!

PORT=3001 npm --prefix frontend-app  start &
PID4=$!

# Store the PIDs in a file for later use
echo $PID1 > flask_pids.txt
echo $PID2 >> flask_pids.txt
echo $PID3 >> flask_pids.txt
echo $PID4 >> flask_pids.txt

echo "Flask servers are running with PIDs: $PID1, $PID2, $PID3"
echo "React servers are running with PID: $PID4"


# Function to stop all Flask servers
stop_servers() {
    echo "Stopping Flask servers..."
    kill $PID1 $PID2 $PID3
    echo "Stopping React server.. "
    kill $PID4
    echo "Waiting for servers to terminate..."
    rm flask_pids.txt
    echo "Flask servers stopped."
    echo "React servers stopped."
}

# Trap signals to ensure the servers are stopped on script termination
trap stop_servers EXIT

# Wait for the user to press Ctrl+C to stop the servers
echo "Press Ctrl+C to stop the servers."
wait




