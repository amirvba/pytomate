import pandas as pd
import numpy as np
import matplotlib
import os


str_file_address = r""
my_df = pd.read_excel(str_file_address)
my_df

df = my_df.copy(deep= True)
df


df_report = pd.DataFrame(np.arange(len(df)), columns = [int_counter, 
                                                        str_file_name,
                                                        int_file_length])
df_report.head()

lst_df_input = []
for i, item in enumerate():
  print(len()-i, item)
  
  my_df = pd.read_excel(str_file_address+"\\"+item)
  lst_df_input.append(my_df)
  
  df_report.loc[i,int_counter] = i
  df_report.loc[i,str_file_name] = item
  df_report.loc[i,int_file_length] = len(my_df)


str_data_name = " - {}.xlsx".format(my_now())
str_save_to = str_file_address + "\\" + str_data_name
print(str_save_to)
.to_excel(str_save_to, index = None)
.head()
