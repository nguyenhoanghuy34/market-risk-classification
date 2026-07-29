import mlflow


def register_model(
    model_uri: str,
    model_name: str,
):

    return mlflow.register_model(
        model_uri=model_uri,
        name=model_name,
    )