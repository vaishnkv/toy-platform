# toy-platform
A toy platform with a React front-end and Flask-based backend services. The backend includes an authentication service, middleware, and core service, all communicating via HTTP. It demonstrates basic full-stack functionality with clear integration between the front-end and backend.


# Motivation :
 For the Company, I work with , most of the time the Platform is down, they didn't have a clue of what is happening. Since I was completely unaware of the "components" that interacting with each other via HTTP. I have decided to build my own toy platform, 
 
# Structure:
  toy_platform comprises of the following components in the specification given below.
    
    0. Front-end:
        - Written in React.
        - There are pages are 
            - login
                - a simple login page with only "signin" option. (will update as we go)
            - Dashboard
                - will greete the user with "Hi {username}". 
                - logout button that will redirect the user back to the login page.
                - The provision to submit the job. This contain the following fields.
                    - job_name: The name of the job.
                    - data : The Actual data that need to be processed by the core-service.
                - A field to see the list of submitted jobs ,along with their status.


    1. Auth Service:
        - Scripted in Python3 and uses Flask for serving HTTP requests.
        - Uses JWT based authentication.
        - Store the UserName and Password in .json file.
        - The endpoints available are :
            - /login - The endpoint where the react-based frontend hits ,when the user tries to login.
    

    2. MiddleWare:
        - Scripted in Python3 and uses Flask for serving HTTP requests.
        - This is where all the requests from the frontend and the core service hits. It contains the following endpoints
            - /job_submit  - The endpoint through which the user can submit the jobs.
            - /job_callback/<job_id>  - Once the job is completed in the core_service, it will hit this endpoint with the necessary metadata.
            - /reset - To reset the middleware. Make the state to the initial state.
            - /list_jobs - The endpoint that will return the list of jobs submitted so far along with their status. 
    
    3. Core_service:
        - Scripted in Python3 and uses Flask for serving HTTP requests.
        - This is where the core_processing happens ,and the business logic resides here.
        - To eliminate the the loss of requests (if many requests arives concurrently) , Used a Simple Queue to store all the requests that yet to be served. This will work in FIFO manner.
        - It contains the following endpoints:
            - /job_submit - To submit a new job to the Queue 
            - /queue_size - Will return the size of the queue (ie , How many requests are yet to get served.)
        
        Note :
            - Usually, In this setting (I mean with Flask) ,people use Celery based Queue ,with Redis to store the requets.
            - Since it is a toy-setting ,The core processing is just string reversal , but simulate the acual processing like situation , I'm deliberately creating a delay with sleep.
        
        - Once a job is finished, it will hit the callback endpoint along with the job_id which was issued by the middleware
    

# Installation:

 Note : 
 - A good practice is to create a Docker file, so that you dont want to think and fix dependency issues, you can just  use off the shelve.
 - Instead of storing the username and password tuples in DB,to keep it simple , I have used a simple .json file to store.
 - To keep it more grounded , I have written bash scripts  
        - To set up the environment (both node and python).
        - To run the servers (both frontend and backend)
 - Assuming that node 16 is available, if not install with nvm using the below command
    > nvm install 16

## steps to follow:

- Once node16 is available. As the first step , we will setup the the environment. For this ,run 
    > chmod +x setup_env.sh <br>
    > ./setup_env.sh

- Once setting up environment is complete, we will run all the servers. For this ,run
    > chmod +x run_servers.sh <br>
    > ./run_servers.sh


# Results:

- The login page will look as follows:
  ![Screenshot 2024-08-23 at 8 18 44 AM](https://github.com/user-attachments/assets/e42bf365-af34-4b9c-be8d-a5a4583d3b59)


- The dashboard will look as follows:
![Screenshot 2024-08-23 at 8 19 48 AM](https://github.com/user-attachments/assets/33d13269-cee8-469b-96bd-80da56c5b11f)

- All the logs are dumped into the log directory








