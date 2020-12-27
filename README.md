# EATender
[![demo image](https://i.imgur.com/3OPL9mf.png)](https://eatender.site/)

## Table of Contents

* **[Technical Detail](#technical-detail)**
  * [Backend](#backend)
  * [Frontend](#frontend)
  * [Database](#database)
  * [Misc](#misc)
* **[Installation](#installation)**
  * [Local Environment](#using-local-environment)
  * [Docker](#using-docker)
* **[License](#license)**


----


## Technical Detail

### Backend

In response to the class requirements, we use Python (3.8.6) as our backend programming language.
We use it for almost all important feature in our project, such as LINE bot handling, Google Maps API connecting, vote sytem, and WEB server creating (We use FastAPI as web framework, for its asynchronous feature allows us to have a better response speed)
As for WSGI, we use Gunicorn with uvicorn workclass as our solution.

### Frontend

Cause we don't have too much time for creating beautiful web UI, we use traditional CSS + JavaScript as a short-term alternative.
We plan to use React or Vue to build web pages that can give users better experience in the future. 
If you are interested, any contribute or PR are welcome :)

### Database

Because of the characteristics of the project content, we use MongoDB as the database solution. Its no-sql features and excellent search functions allow us to achieve an excellent balance between maintenance and performance.

### Misc

In addition to the above, we also use Docker as a tool for program deployment, Nginx as reverse proxy server, and use Github Actions as the CI/CD platform.


----


## Installation

Make sure you have already installed git tools and clone our repo to devices.
```sh
git clone https://github.com/FawenYo/Eatender.git
```


### Using Local Environment

#### Steps

1. First we have to create our own environment variables.
    We use Vim as text editor here.

    ```sh
    cd Eatender
    cd project
    vim .env
    ```
    
    Below is the example enviromment variables, make sure to replace it with your own setting.
    
    LINE_CHANNEL_SECRET={YOUR_OWN_LINE_CHANNEL_SECRET}
    LINE_CHANNEL_ACCESS_TOKEN={YOUR_OWN_LINE_CHANNEL_ACCESS_TOKEN}
    GOOGLE_MAPS_APIKEY={YOUR_OWN_GOOGLE_MAPS_APIKEY}
    MONGO_USER={YOUR_OWN_MONGO_USER}
    MONGO_PWD={YOUR_OWN_MONGO_PWD}
    LINE_NOTIFY_CLIENT_ID={YOUR_OWN_LINE_NOTIFY_CLIENT_ID}
    LINE_NOTIFY_CLIENT_SECRET={YOUR_OWN_LINE_NOTIFY_CLIENT_SECRET}
    LINE_NOTIFY_REDIRECT_URL={YOUR_OWN_LINE_NOTIFY_REDIRECT_URL}
    SITE_NAME={YOUR_OWN_SITE_NAME}

2. Install Python Packages
    ```sh
    pip3 install -r requirements.txt
    ```
3. Time to start up the project!
    You can either to use uvicorn as WSGI
    ```sh
    python3 main.py
    ```
    or use Gunicorn
    ```sh
    gunicorn -c gunicorn.py -k uvicorn.workers.UvicornWorker main:app
    ```


### Using Docker

#### Prerequirements
Make sure you have Docker and Docker-Compose installed!
We use Debian/Ubuntu as example here.
1. Install Docker
    ```su
    sudo apt-get install -y curl
    curl -s https://get.docker.com | sudo sh
    ```
2. Install Docker-Compose
    ```su
    sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    ```
    Go to http://127.0.0.1:8001 and you will see that.
    
#### Steps

1. First we have to create our own environment variables.
    We use Vim as text editor here.

    ```sh
    cd Eatender
    cd project
    vim .env
    ```
    
    Below is the example enviromment variables, make sure to replace it with your own setting.
    
    LINE_CHANNEL_SECRET={YOUR_OWN_LINE_CHANNEL_SECRET}
    LINE_CHANNEL_ACCESS_TOKEN={YOUR_OWN_LINE_CHANNEL_ACCESS_TOKEN}
    GOOGLE_MAPS_APIKEY={YOUR_OWN_GOOGLE_MAPS_APIKEY}
    MONGO_USER={YOUR_OWN_MONGO_USER}
    MONGO_PWD={YOUR_OWN_MONGO_PWD}
    LINE_NOTIFY_CLIENT_ID={YOUR_OWN_LINE_NOTIFY_CLIENT_ID}
    LINE_NOTIFY_CLIENT_SECRET={YOUR_OWN_LINE_NOTIFY_CLIENT_SECRET}
    LINE_NOTIFY_REDIRECT_URL={YOUR_OWN_LINE_NOTIFY_REDIRECT_URL}
    SITE_NAME={YOUR_OWN_SITE_NAME}

2. Get SSL Certificates
    Make sure you have your own domain and go to [SSL For Free](https://www.sslforfree.com/) and place the certificates under /Eatender/nginx 

3. Time to start up the project!
    ```sh
    docker-compose up --build -d
    ```
    Go to http://127.0.0.1 and you will see that.

## License

[The MIT License](LICENSE)

