# api/dependencies.py

from functools import lru_cache

from src.inference.predictor import Predictor


@lru_cache
def get_predictor() -> Predictor:

    return Predictor()