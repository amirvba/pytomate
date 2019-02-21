import os

def get_filenames_with_ending(str_file_address, str_ending):
   
    assert type(str_ending)==str , "The ending must be string!"
    assert type(str_file_address)==str , "The file_address must be string!"
   
    lst_return = []
    lst_filenames = os.listdir(str_file_address)
    
    for str_item in lst_filenames:
        if str_item[:-len(str_ending)]==str_ending:
            lst_return.append(str_item)
            
    return lst_return


# str_ending = 
# str_file_address=
# get_filenames_with_ending(str_file_address, str_ending)
   
def add_space_to_string_if_length_less_than(str_input, int_length):
    
    assert type(str_input)==str, "str_input must be string!"
    assert type(int_length) == int, "int_length must be integer!"
    
    int_dif = int_length - len(str_input)
    if int_dif > 0:
        str_input += " "*int_dif
    return str_input
        
# add_space_to_string_if_length_less_than("sd", 9)



# Source: https://stackoverflow.com/questions/415511/how-to-get-the-current-time-in-python
from time import gmtime, strftime
def my_date():
    str_return = strftime("%Y-%m-%d", gmtime())
    str_return = add_space_to_string_if_length_less_than(str_return, 10)
    
    return str_return

my_date()


from time import gmtime, strftime
def my_time():
    str_return = strftime("%H.%M.%S", gmtime())
    str_return = add_space_to_string_if_length_less_than(str_return, 8)
        
    return str_return
my_time()


def my_now():
    return my_date() +"  "+ my_time()

my_now()
