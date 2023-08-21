FROM python:3.10

RUN apt-get update -y \
    && apt-get upgrade -y pip \
    && pip install --upgrade pip

RUN pip install pandas 
RUN pip install lightgbm scikit-learn
RUN pip install mlflow prefect

WORKDIR /app
COPY USA_cars_datasets_upd.csv.gz USA_cars_datasets_upd.csv.gz
COPY train_model.py train_model.py 