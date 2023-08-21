docker build -t mlflow_test:v01 .

docker run -it \
    --network=mlflow-network \
    -p 5000:5000 \
    mlflow_test:v01 bash

mlflow server --backend-store-uri sqlite:///mlflow.db --host 0.0.0.0