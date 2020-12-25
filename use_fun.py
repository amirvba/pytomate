import pandas as pd
import numpy as np
import matplotlib
import os
import re

#################


def get_excel_files_from_folder(str_file_address=""):
    '''
    This function returns all excel files. Based on MS documentations, 
    there are many excel file extensions:
    .xlsx, .xlsm, .xls, .xlsb, .xltx, .xltm, .xlt, .xls, .xlam, .xla, .xlw, .xlr

    A good solution would be to use regex. Any file name which has the following patterns, 
    will be selected:
    \.xl..$
    \.xl.$

    '''
    lst_return = []
    for item in os.listdir(str_file_address):

        # We remove/neglect files which start with ~, because they are backup file in Windows.
        if bool(re.search('^~', item)):
            continue
        elif bool(re.search('(\.xl..?)$', item.lower())):
            lst_return.append(item)

    return lst_return


def save_excel_from_dictionary(dct_df, str_xl_name, bl_open=False):
    '''
    This function gets a dictionary of data frames and saves them all in a single excel file.
    Sheet names are the same as the keys in the DataFrame.
    indices will be removed. So maybe you would prefer to use the command df.reset_index() before
    saving them in the Dictionary (=dct_df).

    '''
    import os
    assert str_xl_name.endswith(
        ".xlsx"), f'The file name (={str_xl_name}) doesnt end with .xlsx'

    writer = pd.ExcelWriter(str_xl_name, engine='xlsxwriter')

    # Write each dataframe to a different worksheet.
    for key_, value_ in dct_df.items():
        value_.to_excel(writer, sheet_name=key_, index=None)

    writer.save()

    # This only works on windows operating system...
    if bl_open:
        os.system(f'start excel "{str_xl_name}"')

    return True


def reoder_columns(df, lst_ordered, bl_left=True):
    lst_col = [i for i in df.columns if i not in lst_ordered]

    if bl_left:
        lst_col = lst_ordered + lst_col

    else bl_left:
        lst_col = lst_col + lst_ordered

    return df[lst_col]
