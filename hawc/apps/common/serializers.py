from io import StringIO
from typing import Set

from rest_framework import serializers
import pandas as pd


def validate_csv(value: str, expected_columns: Set) -> pd.DataFrame:
    """
    Validates a data-string as a pandas parasable CSV in the expected format.

    Args:
        value (str): The input data
        expected_columns (Set): A set of column names

    Returns:
        pd.DataFrame: The validated dataframe
    """
    try:
        df = pd.read_csv(StringIO(value))
    except pd.errors.ParserError:
        raise serializers.ValidationError("CSV could not be parsed")
    except pd.errors.EmptyDataError:
        raise serializers.ValidationError("CSV must not be empty")

    # ensure columns are expected
    if set(df.columns.tolist()) != expected_columns:
        raise serializers.ValidationError(
            f"Invalid column headers; expecting \"{','.join(expected_columns)}\""
        )

    # ensure we have some data
    if df.shape[0] == 0:
        raise serializers.ValidationError("CSV has no data")

    # ensure we don't have duplicates in our data
    if df.duplicated().any():
        raise serializers.ValidationError("CSV has duplicate rows")

    return df
