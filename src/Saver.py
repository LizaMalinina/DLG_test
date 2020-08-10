import pandas as pd


def save_to_parquet(df: pd.DataFrame, base_path: str, partition_by_ymd=True) -> None:
    if partition_by_ymd:
        # Note: In a real world scenario I would use pySpark instead of Python for multiple reasons and use overwrite
        # mode while writing to parquet
        df.to_parquet(base_path, partition_cols=['year', 'month', 'day'])
    else:
        df.to_parquet(base_path + 'temp.parquet')
