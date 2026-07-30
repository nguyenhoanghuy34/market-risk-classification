import mlflow
import mlflow.sklearn

from config import (
    MLFLOW_TRACKING_URI,
    MLFLOW_ARTIFACT_ROOT,
    MLFLOW_EXPERIMENT_NAME,
)


class MLflowTracker:

    def __init__(self):

        mlflow.set_tracking_uri(
            MLFLOW_TRACKING_URI
        )

        experiment = mlflow.get_experiment_by_name(
            MLFLOW_EXPERIMENT_NAME
        )

        if experiment is None:

            mlflow.create_experiment(
                name=MLFLOW_EXPERIMENT_NAME,
                artifact_location=MLFLOW_ARTIFACT_ROOT.resolve().as_uri(),
            )

        mlflow.set_experiment(
            MLFLOW_EXPERIMENT_NAME
        )


    def start_run(
        self,
        run_name=None,
    ):

        return mlflow.start_run(
            run_name=run_name
        )


    def log_params(
        self,
        params,
    ):

        mlflow.log_params(
            params
        )


    def log_metrics(
        self,
        metrics,
    ):

        mlflow.log_metrics(
            metrics
        )


    def log_model(
        self,
        model,
    ):

        mlflow.sklearn.log_model(
            model,
            name="model",
        )