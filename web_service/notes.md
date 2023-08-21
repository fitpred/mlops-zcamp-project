pip freeze | grep scikit-learn

pipenv install pandas==2.0.3 scikit-learn==1.3.0 lightgbm==4.0.0 cffi==1.15.1 flask --python=3.10

pipenv shell

PS1="> "

pipenv install mlflow # to load model.pkl file (ModuleNotFoundError: No module named 'mlflow')
pipenv install gunicorn

gunicorn --bind=0.0.0.0:9696 predict:app


pipenv install --dev requests


docker build -t car-price-prediction-service:v1 .


docker run -it --network=mlflow-network --rm -p 9696:9696 car-price-prediction-service:v1


docker run -it --rm -p 9696:9696 car-price-prediction-service:v1


EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app" ]

    command: gunicorn --bind=0.0.0.0:9696 predict:app
    