import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import numpy as np
import os
import re


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

    
    
# The following two functions can be used for Root Cause Analysis:
def augment_reason(DF, index_reason, str_reason):
    
    for item in ['reason', 'tried hypothesis']:
        if item not in DF.columns:
            DF[item] = np.nan
            print(f"Column '{item}' added to DataFrame.")
    
    index_final = DF['reason'].isna() & index_reason
    DF.loc[index_final, 'reason'] = str_reason
    DF.loc[index_reason, 'tried hypothesis'] = DF.loc[index_reason, 'tried hypothesis'].map(str) + " | " + str_reason

    print("-----------------------")
    print("reason \t|", str_reason)
    print(index_reason.sum(), " \t| Count of rows affected by the reason.")
    print( index_final.sum(), " \t| Count of rows affected by the reason, which werent affected already.")
    print(DF['reason'].isna().sum(), " \t| Count of remaining rows.")
    
    return DF


def augment_comment(DF, index_comment, str_comment):
    '''
    This function adds comments to the rows, which we havent found any reason for them.
    These comment can show our guess about the values. If for example they are dupplicated but we dont know why,
    it would be good to write it in the comments. It helps to resume the analysis in a meeting.
    '''    
    assert 'reason' in DF.columns, f"The column reason doesnt exist in the DataFrame."
    index_final = DF['reason'].isna() & index_comment
    DF.loc[index_final, 'comment'] = str_comment
    
    index_no_comment_no_reason = DF['reason'].isna() & ~index_comment
    
    
    print("-----------------------")
    print("comment |", str_comment)
    print(index_comment.sum(), " \t| Count of rows affected by the comment.")
    print(index_no_comment_no_reason.sum(), " \t| Count of remaining uncommented AND not reasoned rows.")
    
    return DF


# Sankey example
from ipysankeywidget import SankeyWidget

links = [
    {'source': 'start', 'target': 'A', 'value': 2, 'type': 'y'},
    {'source': 'start', 'target': 'B', 'value': 20},
    {'source': 'B', 'target': 'C', 'value': 5, 'type': 'x'},
    {'source': 'B', 'target': 'D', 'value': 15, 'type': 'x'},
]

SankeyWidget(links=links, margins=dict(top=0, bottom=0, left=50, right=100),  linkLabelFormat='.0f')




time_start = datetime.now()

def get_deltatime_in_seconds(time_start):
    return (datetime.now()-time_start).seconds

def convert_seconds__days_hours_minutes_seconds(td):
    str_return =  {'day': td//(60*60*24)%30
              , 'hour':td//(60*60)%24
              , 'minute':(td//60)%60
              , 'second':td%60
              }
#     print(str_return)
    return str_return

def get_duration_in_days_hours_minutes_seconds(start_time):
    duration_in_seconds = get_deltatime_in_seconds(start_time)
    
    return convert_seconds__days_hours_minutes_seconds(duration_in_seconds)
    
# get_duration_in_days_hours_minutes_seconds(start_time)


def get_dct_log():
    import getpass
    from datetime import datetime

    return {'start_time': datetime.now(), 'Ran by': getpass.getuser(), 'Current working directory': os.getcwd()}
