# powerplant-coding-challenge

## Intro
Solution of the coding challenge that allocates sources of electric power based on a list of available power plants.

## Structure of the project
The project contain server that solves the problem as well as client that delivers problems to the server. Beside that additional files defining Docker contained, Python virtual environment and additional helper files are associated.  

### Files
 - server.py - Definition of the server
 - client.py - Helper client
 - powerplant_payload.py - Problem solver
 - Dockerfile - Definition of the docker image
 - poetry.lock + pyproject.toml - Definition of the Python virtual environment
 - install.sh - Installer of dependencies on Docker image
 - run.sh - Scripts that starts the server in a container

## Installation of the dependencies of the Python environment
Dependencies of the Python files are contained in Python virtual environment that is operated by poetry. To create virtual environment and to update and to install dependencies script install.sh can be used.  

### Triggering server without Docker container
Triggering the server can be done using run.sh script. The server operates at port 8888 on a local machine at the end-point productionplan using POST method. It replays back to the client allocation of the power plants in JSON format.  

### Triggering server in Docker container
To employ Docker we need to create an image and then to deploy the container. Build process can be executed using 
`docker build -t server .` and deployment using command `docker run -P --name challenge-server server:latest`.

### Testing the server
To test deployed server we use script _client.py_. In a terminal, we trigger installation script *install.py* if it was not started alread. And then, Python environment is activated with command `source challenge-env/bin/activate`. The environment is prepared for the client that is triggered by command `python3 client.py`. Based on the deployment of the server we need to use **localhost_url** or **docker_url** variable on line 17 of _client.py_. It should be noted that the IP of docker may vary based in system configuration.    

## Conclusions
The application demonstrates simple Python web server that calculates predictions of the allocations of power plants to meet required load.  
