FROM python:3.10

RUN apt-get update -y \
    && apt-get upgrade -y pip \
    && pip install --upgrade pip

RUN pip install mlflow prefect lightgbm

WORKDIR /model

WORKDIR /app
COPY register_model.py register_model.py 

ENTRYPOINT [ "python", "register_model.py" ]