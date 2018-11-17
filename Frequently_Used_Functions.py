import os

def get_filenames_with_ending(str_file_address, str_ending):
    
    assert type(str_ending)==str , "The ending must be string!"
    assert type(str_file_address)==str , "The file_address must be string!"
    
    
    lst_return = []
    lst_filenames = os.listdir(str_file_address)
    
    for str_item in lst_filenames:
        if str_item[:len(str_ending)]==str_ending:
            lst_return.append(str_item)
            
    return lst_return
