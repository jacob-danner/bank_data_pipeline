import os
from zipfile import ZipFile

def get_zip_name():
    filenames = os.listdir()
    zip_fname = None
    
    for f_name in filenames:
        if '.zip' in f_name:
            zip_fname = f_name

    return zip_fname

def unzip(zip_file):
    zip_id = zip_file.split()[-1] # grabs 03312022.zip
    zip_id = zip_id[:-4] # grabs 03312022
    cwd = os.getcwd()
    data_dir = f'{cwd}/{zip_id}'
    os.mkdir(data_dir)

    with ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(data_dir)

    return data_dir
        
'''
functions below: helper functions for clean_dir()
'''

def clean_element(el):
    # get substring between ()
    start = el.find('(')
    stop = el.find(')') + 1
    to_replace = el[start:stop]

    part_num = ' ' + to_replace[1]

    el = el.replace(to_replace, part_num)
    return el

def get_old_and_cleaned(filename_lengths):
    files_with_parts = [x for x in filename_lengths if filename_lengths[x] == 8]
    other_files      = [x for x in filename_lengths if filename_lengths[x] != 8]

    old_names = files_with_parts + other_files

    files_with_parts = [clean_element(x) for x in files_with_parts]
    clean_list = files_with_parts + other_files

    return old_names, clean_list 

def remove_junk(el):
    el = el.split()
    important = el[2:]
    final_name = '_'.join(important)

    return final_name

def get_pairs(old_names, cleaned_names):
    pairs = []
    for i in range(len(old_names)):
        row = (old_names[i], cleaned_names[i])
        pairs.append(row)

    return pairs

def make_new_names(dir):
    files = os.listdir(dir)
    filename_lengths = {x: len(x.split()) for x in files} # length indicates imporant attributes about a file
    old_names, cleaned_names = get_old_and_cleaned(filename_lengths)
    cleaned_names = [remove_junk(el) for el in cleaned_names]

    old_new_pairs = get_pairs(old_names, cleaned_names)

    return old_new_pairs

def clean_dir(dir):
    os.remove(f'{dir}/Readme.txt') # delete readme
    names = make_new_names(dir)
    for old, new in names:
        os.rename(f'{dir}/{old}', f'{dir}/{new}')