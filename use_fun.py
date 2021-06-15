import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import numpy as np
import os
import re

from xlwings import view
import xlwings as xw
import warnings
warnings.filterwarnings('ignore')


%config Completer.use_jedi = False


def conv_seconds_2_time_stamp(str_in):
    
    hours_ = str_in // (60*60)
    str_in = str_in - hours_*60*60
    
    minutes_ = str_in // (60)
    seconds_ = str_in - minutes_*60

    seconds_ = round(seconds_, 1)

    return f'{int(hours_)}:{int(minutes_)}:{seconds_}'
    
# conv_seconds_2_time_stamp(43200)


def print_lst(lst_, sep_ = " \t| "):
    lst_ = [str(i) for i in lst_p]
    print(sep_.join(lst_))
    
   
def get_fig_frequency(DF, lst_col, title = None, fig_size_x =  18.5, fig_size_y = 10.5):
    
    assert len(lst_col)>0, "List of columns is empty."
    assert [i for i in lst_col if i not in DF.columns] == [], "The list of column was not in the list of DF columns!"
    
    if len(lst_col)==1:
        print("Because of an interal bug, we generate the plots twice!")
        lst_col = lst_col + lst_col
        
    plt.style.use('ggplot')

    fig, axs = plt.subplots(len(lst_col),2)

    if title is not None:
        fig.suptitle(title)

    for i, col in enumerate(lst_col):
        print(i,col)
        axs[i,0].boxplot(DF[col])
        axs[i,0].set_title(col)

        axs[i,1].hist(DF[col])
        axs[i,1].set_title(col)

    fig.set_size_inches(fig_size_x, fig_size_y)
                                          
    return fig
                  
    
def to_excel_from_dct(dct_df, file_name, add_time_tag = False, close_workbook = False, dct_fig = None):

    import xlwings as xw
    import os
    
    wb = xw.Book()
    
    xlSrcRange = 1
    xlYes = 1

    lst_sheets = []

    str_assert = "The sheet names can only have 31 charachter. We are only allows to use this part:\n"
    if dct_fig:
        for name_ in sorted(dct_fig.keys(), reverse=True):
            assert len(name_)<=31, str_assert + f"\n{name_[:31]}"
            
            lst_sheets.append(name_)
            sh = wb.sheets.add(name_)
            sh.pictures.add(dct_fig[name_], name=name_, update=True)

        print("Figures \t| Successfully added")
    
    for name_ in sorted(dct_df.keys(), reverse=True):
        
        assert len(name_)<=31, str_assert + f"\n{name_[:31]}"
        lst_sheets.append(name_)
        sh = wb.sheets.add(name_)
        sh.range('A1').options(index = None).value =  dct_df[name_]

        tbl_range = sh.range("A1").expand('table')
        sh.api.ListObjects.Add(xlSrcRange, tbl_range.address, 0, 1).Name = f"tbl_{name_}"
        sh.autofit(axis="columns")

    print("DataFrames \t| Successfully added")


    for sheet in [sh.name for sh in wb.sheets]:
        if sheet not in lst_sheets:
            print(sheet, "\t| deleted")
            wb.sheets[sheet].delete()
                
    if add_time_tag:
        from datetime import datetime 
        file_name = file_name.replace(".xlsx", "")
        file_name += " -- " + datetime.now().strftime("%Y-%m-%d %H.%M.%S") + ".xlsx"
        
    print(f'\nPath: \t\t| {os.getcwd()}')
    print(f'Filen name: \t| {file_name}')
    
    wb.save(file_name) 
    if close_workbook:
        wb.close()
        
    return file_name

to_excel_from_dct(dct_df, f"{str_xl_name} ++ fuzyy", add_time_tag = True, close_workbook = False)


def value_counts(DF, str_column):
    return (pd.DataFrame(DF[str_column]
             .value_counts(dropna=True))
             .reset_index()
             .rename(columns = {str_column:'count'
                               , 'index':str_column})
            )


# value_counts(df, 'abfahrt_anzahl')

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


def get_common_words_in_column(DF, str_col):

    set_base = set(DF[str_col][0].lower().split(" "))

    for item in DF[str_col]:
        set_row = set(item.lower().split(" "))
        set_base = {item for item in set_row if item in set_base}

        if set_base == {}:
            return set_base
        
    return set_base

def filter_df_based_on_list_of_search_words(DF, lst_search_words):
    
    lst_search_words = [i for i in lst_search_words if i is not ""]
    assert '' not in lst_search_words, f'There was an empty string in the list. This returns every row!, remove it!'
    return DF[DF['target'].apply(lambda sentence: any(word in sentence for word in lst_search_wordds))]
    
