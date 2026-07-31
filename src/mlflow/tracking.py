import mlflow
import mlflow.sklearn
import mlflow.keras
import mlflow.xgboost

from xgboost import XGBClassifier, XGBRegressor, Booster

from config import (
    MLFLOW_TRACKING_URI,
    MLFLOW_ARTIFACT_ROOT,
    MLFLOW_EXPERIMENT_NAME,
)

from src.utils.mlflow_summary import (
    main as generate_mlflow_summary,
)


class MLflowTracker:

    def __init__(self):

        # ============================
        # MLflow Tracking URI
        # ============================

        mlflow.set_tracking_uri(
            MLFLOW_TRACKING_URI
        )

        # ============================
        # Create Experiment If Missing
        # ============================

        experiment = mlflow.get_experiment_by_name(
            MLFLOW_EXPERIMENT_NAME
        )

        if experiment is None:

            mlflow.create_experiment(
                name=MLFLOW_EXPERIMENT_NAME,
                artifact_location=(
                    MLFLOW_ARTIFACT_ROOT
                    .resolve()
                    .as_uri()
                ),
            )

        mlflow.set_experiment(
            MLFLOW_EXPERIMENT_NAME
        )

    # ============================
    # Start Run
    # ============================

    def start_run(
        self,
        run_name=None,
    ):

        return mlflow.start_run(
            run_name=run_name
        )

    # ============================
    # Log Parameters
    # ============================

    def log_params(
        self,
        params,
    ):

        mlflow.log_params(
            params
        )

    # ============================
    # Log Metrics
    # ============================

    def log_metrics(
        self,
        metrics,
    ):

        mlflow.log_metrics(
            metrics
        )

    # ============================
    # Log Model
    # ============================

    def log_model(
        self,
        model,
    ):

        model_type = str(
            type(model)
        ).lower()

        # ----------------------------------
        # TensorFlow / Keras
        # ----------------------------------

        if (
            "keras" in model_type
            or "tensorflow" in model_type
        ):

            mlflow.keras.log_model(
                model,
                name="model",
            )

        # ----------------------------------
        # XGBoost
        # ----------------------------------

        elif isinstance(
            model,
            (
                XGBClassifier,
                XGBRegressor,
                Booster,
            ),
        ):

            mlflow.xgboost.log_model(
                model,
                name="model",
            )

        # ----------------------------------
        # Scikit-learn
        # ----------------------------------

        else:

            mlflow.sklearn.log_model(
                model,
                name="model",
            )

    # ============================
    # Generate Summary
    # ============================

    def generate_summary(
        self,
    ):

        generate_mlflow_summary()