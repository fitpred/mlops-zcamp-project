# MLOps-zoomcamp-project


# 1. Project description
For my project I used **USA cars dataset** that contains information about cars with milage: brand, model, year, mileage, price, etc
https://github.com/rashida048/Datasets/blob/master/USA_cars_datasets.csv

So imagine you work for car dealer that buy and sell used cars. Business is growing and managers ask you for help to define the price of the cars in order to speed up buying process

The task is build web service that accept information about the car and return estimated price.

Note: as well as the datasource containes only 2500 rows I augmented data (just by adding some Gaussian noise) to make it looks like real world task, because usually you don't need ML to deal with such small amount of data


# 2. Prerequisites
- AWS account, IAM user with access to AWS Beanstalk, aws key id, aws secret key
- Prefect cloud account, api key, export it to enviroment " export PREFECT_API_KEY = '' "
- Docker, Docker compose


# 3. Tech stack
- Cloud: **AWS EC2, AWS Elastic Beanstalk**
- ML experiment tracking:  **Mlflow**
- Workflow Orchestration: **Prefect Cloud**
- Containerization: **Docker, Docker compose**


# 4. Reproducibility
There are two main parts of the project: **train model** and **deploy it**. Below you can find step-by-step guide to reproduce the project, but here is brief overview *(I assumed that you cloned repo and moved to root directory)*:

   ### **Train model**

   There are 3 docker containers to train model: mlflow, train_model, register_model. Data for training is saved in *train* folder - *USA_cars_datasets_upd.csv.gz* 

   You can train your model on **remote host** as well as **localy** (but if your OS is Windows you need to change paths in docker-compose.yaml file: in **build** section you should specify full path to folders: *mlflow*, *train_model*, *register_model*)

   If you decided to use your local computer and you have docker, docker-compose installed - **all that you need is run docker compose: docker-compose up** *(remember that you need to export PREFECT_API_KEY before)*

   It will run 3 containers in turn:
   - launch mlflow server, 
   - train_model - run train model script with connection to mlflow server and prefect cloud
   - register_model - choose the best model by MAE, register it and promote to production, than save it to *web_service* folder.

   So when the last container register_model finishes, you can open mlflow ui 127.0.0.1:500, find experiments as well as production model in model registry. Also you'll see *model.pkl* file in web_service folder

   **Deploy model**

   When the first step is done you can deploy you model

   To deploy the model go to **web_service** folder and run make file: **make deploy**
   It will deploy docker container with production model, install awsebcli, create project in AWS Elastic Beanstalk and deploy container to it

   *If you run makefile from local computer you should specify aws keys*


# 5. Walkthrough instruction
1. Create AWS EC2 instance (I took Ubuntu 22.04 lts)
2. Connect to it: ssh -i file.pem username@ip-address
3. Install Docker, Docker compose, add your user to docker group, install pip, export prefect PREFECT_API_KEY
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



eb terminate car-price-env-new