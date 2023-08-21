docker build -t train_test:v01 .

docker run -it \
    --network=mlflow-network \
    train_test:v01 bash