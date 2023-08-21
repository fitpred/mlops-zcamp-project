# MLOps-zoomcamp-project


## Project description
For my project I used USA cars dataset that contains information about cars with milage: brand, model, year, mileage, price, etc
https://github.com/rashida048/Datasets/blob/master/USA_cars_datasets.csv

So imagine you work for car dealer that buy and sell used cars. Business is growing and managers ask you for help to define the price of the cars in order by speed up buying process

The task is build web service that accept information about the car and return estimated price.

As well as the datasource containes only 2500 rows I augmented data (just by adding some Gaussian noise) to make it looks like real world task (usually you don't need ML to deal small amount of data)


## Prerequisites
AWS account, aws key id, aws secret key
Prefect cloud account, workspace id,  account id, api key


## Tech stack
Cloud: AWS Elastic Beanstalk (deploy web app)
ML experiment tracking tool:  Mlflow
Orchestration: Prefect Cloud
Docker, Docker compose


## Reproducibility
Main steps:
   - create AWS EC2 instance
   - ssh to it, install docker, docker-compose, clone repository
   - prepare prediction model by running docker compose
   - deployin that model to cloud

Below you find step-by-step guide to reproduce the project


first step is dockerized and fully automated


 - run docker-compose that contains things:
   - run mlflow server
   - train model
   - register model, promote to production
   - run web service local to test it (and deploy on aws later)
 - deploy the best model (or model of your choise) to the cloud


ssh -i file.pem username@ip-address



## walkthrough instruction
1. Create AWS EC2 instance (I took Ubuntu 22.04 lts)
2. Connect to it: ssh -i file.pem username@ip-address
3. Install pip, Docker, Docker compose, add your user to docker group: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04
4. Create projects folder, go to it and clone repo
5. Launch Mlflow server, connect to prefect cloud, train model and register it: (all this done in docker compose)
   go to project root folder and run docker-compose up - it will launch mlflow server, run train model scripts connected to mlflow server and prefect cloud, register model and save it to web-service folder. If you want to open mlflow UI on your laptop, you should forward port 5000
6. Build docker container to deploy: go to web-service folder, run: docker build -t car-price-prediction-service:v1 .
7. Test it by: 
   - running docker container with service: docker run -it --rm -p 9696:9696 car-price-prediction-service:v1
   - go to project root directory and send request: python3 request_test.py (you can play with requested parameters)
8. Prepare AWS Elastic Beanstalk for deploying: 
   - on AWS create IAM user with access to Elastic Beanstalk service and create secret key
   - on your host machine install awsebcli (pip install awsebcli), check installation by eb --version (1)
   - go to web-service folder and run eb init and follow the prompts(2)
9. Test it localy by: 
   running service: eb local run --port 9696 (make sure port 9696 is not busy)
   sending request: python3 request_test.py
10. Deploy on AWS: eb create car-price-env
   After that you cat go to AWS website to Elastic Beanstalk service, Here you'll see your service is up and running. Also you can find 
   WARNING: this service is open for the world, so don't forget to stop it by: eb terminate car-price-env
11. Now you can access your service from anywere by domain that you can find in Elastic Beanstalk - Applications - car-price-prediction-service.
   For example, copy request_test.py to your laptop, change "host" to domain you've got and run it: python request_test.py




(1) if it says eb: command not found you need to:
   export PATH="/usr/local/bin:$PATH"
   source .profile

(2) prompts:
      - enter your region
      - enter you access id and secret key
      - set application name (car-price-prediction-service)
      - enter Y as anwer on question "It appears you are using Docker/ Is this correct?"
      - select a platform branch (I went with 1 - Amazon Linux 2023)
      - set up ssh for your instance - as you wish, I said no


P.S. You can reproduce steps 1-7 localy, but if your OS is Windows, you'll need to change paths in docker-compose.yaml file





