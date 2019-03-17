import pandas as pd
import numpy as np
import matplotlib
import os


str_file_address = r""
my_df = pd.read_excel(str_file_address)
my_df

df = my_df.copy(deep= True)
df

#################
import os

def get_filenames_with_ending(str_file_address, str_ending):
   
    assert type(str_ending) == str , "The ending must be string!"
    assert type(str_file_address) == str , "The file_address must be string!"
   
    lst_return = []
    lst_filenames = os.listdir(str_file_address)
    
    for str_item in lst_filenames:
        if str_item[-len(str_ending):]==str_ending:
            lst_return.append(str_item)
            
    return lst_return

 
str_ending = ".csv"
str_file_address = r""
lst_all_files = get_filenames_with_ending(str_file_address+ "\\", str_ending)
#print(lst_all_files)
print(len(lst_all_files))
lst_all_files[:5]

df_report = pd.DataFrame(np.arange(len(lst_all_files)), columns = [str_counter, 
                                                                    str_file_name,
                                                                    int_file_length,
                                                                  int_duration])
df_report.head()

lst_df_input = []
for my_counter, item in enumerate(lst_all_files):
  print(len()-my_counter, item)
  
  my_df = pd.read_excel(str_file_address+"\\"+item)
  lst_df_input.append(my_df)
  
  df_report.loc[my_counter,int_counter] = my_counter
  df_report.loc[my_counter,str_file_name] = item
  df_report.loc[my_counter,int_file_length] = len(my_df)


str_data_name = " - {}.xlsx".format(my_now())
str_save_to = str_file_address + "\\" + str_data_name
print(str_save_to)
df_report.to_excel(str_save_to, index = None)
df_report.head()


str_msg = "Hello everyone,\n\n"

str_msg += "{} \t| Number of files\n".format()
str_msg += "{} \t| \n".format()
str_msg += "{} \t| \n".format()

str_msg += "{} s. \t| Duration \n".format(df_report['int_duration'].sum())
str_msg += "{} \t| The script was run by the user\n\n".format()


str_msg += "Best regards"
