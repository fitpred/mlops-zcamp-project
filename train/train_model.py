import pandas as pd
import mlflow
from prefect import flow, task
import lightgbm as lgb


from sklearn.metrics import mean_absolute_error


MLFLOW_TRACKING_URI = "http://mlflow_server:5000" # "http://127.0.0.1:5000" 

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("usa_cars_price_prediction")


cat_cols = ['brand', 'title_status', 'state']
num_cols = ['year', 'mileage']


# read data
@task(retries=3, retry_delay_seconds=30)
def read_data(filename):
    """Read data into DataFrame"""
    df = pd.read_csv(filename)

    return df


@task
def train_test_split(dataframe):

    feature_cols = cat_cols + num_cols

    for i in cat_cols:
        dataframe[i] = pd.Series(dataframe[i], dtype="category")    

    X_train = dataframe[:1500][feature_cols]
    y_train = dataframe[:1500]['price']

    X_val = dataframe[1500:][feature_cols]
    y_val = dataframe[1500:]['price']

    return X_train, X_val, y_train, y_val


@task(log_prints=True)
def train_model(X_train, X_val, y_train, y_val):

    alpha_list = [0.001, 0.005, 0.01, 0.025, 0.05, 0.1]

    for alpha in alpha_list:

        with mlflow.start_run():

            mlflow.log_param("alpha", alpha)

            gbm = lgb.LGBMRegressor(learning_rate=alpha, n_estimators=1000)

            gbm.fit(X_train, y_train,
                    eval_set=[(X_val, y_val)], 
                    eval_metric='mae',
                    categorical_feature=cat_cols,
                    callbacks=[
                        lgb.early_stopping(200), 
                        lgb.log_evaluation(-1)
                    ],  
                    )

            y_pred = gbm.predict(X_val)
            mae = mean_absolute_error(y_val, y_pred)
            mlflow.log_metric("mae", mae)

            mlflow.lightgbm.log_model(gbm, artifact_path="data/models")

            mlflow.end_run()

    return None


@flow(retries=3, retry_delay_seconds=30)
def main_flow(filename='USA_cars_datasets_upd.csv.gz'):

    """The main training pipeline"""

    # MLflow settings
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("usa_cars_price_prediction")

    # load data 
    df = read_data(filename)

    # train test split
    X_train, X_val, y_train, y_val = train_test_split(df)

    # train model
    train_model(X_train, X_val, y_train, y_val)


if __name__ == "__main__":
    main_flow()








