import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType
from prefect import flow
import pickle


MLFLOW_TRACKING_URI = "http://mlflow_server:5000"  # "http://127.0.0.1:5000"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("usa_cars_price_prediction")

client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)


@flow(retries=3, retry_delay_seconds=30)
def register_model():

    # get run id of the best model
    runs = client.search_runs(
        experiment_ids='1',
        run_view_type=ViewType.ACTIVE_ONLY,
        order_by=["metrics.mae ASC"]
    )

    run_id = runs[0].info.run_id

    print(f'run id: {run_id}')


    # register model
    model_name = "best-model-usa-cars-price-predictor"

    model_uri = f"runs:/{run_id}/models"
    mlflow.register_model(model_uri=model_uri, name=model_name)

    latest_versions = client.get_latest_versions(name=model_name)


    model_version = latest_versions[0].version
    new_stage = "Production"

    client.transition_model_version_stage(
        name=model_name,
        version=model_version,
        stage=new_stage
    )


    logged_model = f'runs:/{run_id}/data/models'
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    with open('../model/model.pkl', 'wb') as f_out:
        pickle.dump(loaded_model, f_out)


    print(f'model: {run_id} promoted to production')



if __name__ == "__main__":
    register_model()