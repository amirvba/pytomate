import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import numpy as np
import os
import re


def augment_reason(DF, index_reason, str_reason):
        
    if 'reason' not in DF.columns:
        DF['reason'] = np.nan
        print("Column 'reason' added to DataFrame.")
        
    
    index_final = DF['reason'].isna() & index_reason
    DF.loc[index_final, 'reason'] = str_reason
    DF.loc[index_reason, 'reason_incremental'] = DF.loc[index_reason, 'reason_incremental'].map(str) + " | " + str_reason

    print("-----------------------")
    print("reason \t|", str_reason)
    print(index_reason.sum(), " | Count of rows affected by the reason.")
    print( index_final.sum(), " | Count of rows affected by the reason, which werent affected already.")
    print((~index_final).sum(), " | Count of remaining rows.")
    
    return DF


def get_df_log(dct_log, lst_rows_top = [], lst_rows_down = []):
    
    if 'script started at' in dct_log.keys():
        dct_log['script duration'] = str(datetime.now() - dct_log['started_at'])
        dct_log['script started at'] = str(dct_log['script started at'])
    
    df_log = pd.DataFrame([dct_log])
    
    df_log = reoder_columns(df_log, lst_rows_top , bl_left=True)
    df_log = reoder_columns(df_log, lst_rows_down, bl_left=False)
    
    df_log = df_log.T.reset_index()                                
    df_log.rename(columns = {'index':'key', 0:'value'}, inplace= True)
    
    return df_log



def get_now(): 
    from datetime import datetime 
    return datetime.now().strftime("%Y-%m-%d %H.%M.%S") 


def get_time(): 
    from datetime import datetime 
    return datetime.now().strftime("%H.%M.%S") 


def get_date(): 
    from datetime import datetime 
    return datetime.now().strftime("%Y-%m-%d") 


def get_files(filepath, str_ending = '*.json'):
    lst_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, str_ending))
        for f in files:
            lst_files.append(os.path.abspath(f))
    
    return lst_files


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
        return df[lst_ordered + lst_col]

    else:
        return df[lst_col + lst_ordered]
