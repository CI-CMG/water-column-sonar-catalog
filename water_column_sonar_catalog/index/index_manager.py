import pandas as pd

MAX_POOL_CONNECTIONS = 64
MAX_CONCURRENCY = 64
MAX_WORKERS = 64
GB = 1024**3


class IndexManager:

    def __init__(self, input_bucket_name, calibration_bucket, calibration_key):
        self.input_bucket_name = input_bucket_name
        self.calibration_bucket = calibration_bucket

    #################################################################
    @staticmethod
    def get_ek60_objects(df: pd.DataFrame, subset_datagrams: list) -> pd.DataFrame:
        pass
