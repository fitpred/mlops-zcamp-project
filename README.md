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



## walkthrough
1 Create AWS EC2 instance (I took Ubuntu 22.04 lts)
2 ssh to it: ssh -i file.pem username@ip-address
3 install Docker, Docker compose, add your user to docker group: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04
4 Create projects folder, go to it and clone repo
5 go to project root folder and 



1 git clone  repository 
2 in project root folder create .env file with aws and prefect keys
3 run docker-compose up
   by runnig docker compose you're:
   - launching mlflow server - src/mlflow
   - optimize hyperparams and train model - src/train (with using Mlflow as experiment tracking service and Prefect as a workflow orchestration - so you are able to see models on http://127.0.0.1:5000, and train workflow on prefect cloud in a workspace you created)
   - register best model and promote it to production - src/register_model (model pickle file will be created and saved to web_service folder for deploying)
   - run deployed service with gunicorn server
4 test service by running "python request_test.py"

In terms of model tuning - I just tried different alpha params for the simplicity

P.S. Ff your OS is windows and you want to run project localy, you need to change paths in docker compose



pipenv install awsebcli --dev
pip install awsebcli
pip install mlflow








# ssh to aws instance
ssh -i .aws/mlops-zcamp-project.pem ubuntu@ec2-54-208-232-243.compute-1.amazonaws.com








create aws account
create account on prefect cloud 
   create project
   create API_KEY keys
   save it to .env file in project root directory
install docker, docker-compose
 - create Prefect cloud acctount
    - create workspace




eb init 
follow the prompt
 - enter your region
 - enter you access id and secret key
 - set application name
 - enter Y as anwer on question "It appears you are using Docker/ Is this correct?"
 - select a platform branch (I went with 1 - Amazon Linux 2023)
 - set up ssh for your instance - as you wish, I said no


car-price-prediction-service


-p docker -r us-east-1 car-price-service


# run localy
eb local run --port 9696

# create eb enviroment
eb create car-price-env

Attention: this service will be available for the hole world, so don't forget to stop it


# terminate eb enviroment
eb terminate car-price-env


you could be charged while working with AWS services, but not significant
