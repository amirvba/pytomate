from datetime import datetime
import pandas as pd
import numpy as np

def test_same_column_name(DF1, DF2):
    assert set(DF1.columns) == set(
        DF2.columns), "Column names are not the same."


def test_same_df_length(DF1, DF2):
    assert len(DF1) == len(DF2), "DataFrames dont have the same length."


def get_df_diff(DF_1, DF_2, str_column):
    '''Finds differences between two DF based on outer join and the argument indicator=True.'''
    
    df_joined = DF_1.merge(DF_2, on=str_column, how='outer', indicator=True)
    return df_joined[df_joined['_merge'] != 'both']


def test_get_df_diff(DF_1, DF_2, str_column):

    df_temp = get_df_diff(DF_1, DF_2, str_column)
    str_assert = f'There are differences in the column "{str_column}" between the two DataFrames.\n'
    str_assert += 'Run get_df_diff() with the same arguments to know more.'
    assert len(df_temp) == 0, str_assert
