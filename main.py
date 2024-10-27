from bs4 import BeautifulSoup
import json
import re
import os
from datetime import datetime

# reads a lokal tiddlywiki file, extracts content tiddlers and writes each tiddler content to a single file

tiddly_wiki_file = 'schniki.html' # name pf tiddlywiki to export files
ignore_types = ["image/png"] # ignore certain tiddler types
maximum_file_name_length = 220 # max length of file name
export_directory = "export" # name of folder where files will be stored. folder gets created if not exist
exportet_file_extension = "txt" # txt or md
exportet_file_tiddler_contents = ["title", "text", "tags"] # tiddler fields content, which get written in the exportet file

# functions
def clean_string(string):
    """
    Removes umlauts from strings and replaces them with the letter+e convention
    """
    u = 'ü'.encode()
    U = 'Ü'.encode()
    a = 'ä'.encode()
    A = 'Ä'.encode()
    o = 'ö'.encode()
    O = 'Ö'.encode()
    ss = 'ß'.encode()

    string = string.encode()
    string = string.replace(u, b'ue')
    string = string.replace(U, b'Ue')
    string = string.replace(a, b'ae')
    string = string.replace(A, b'Ae')
    string = string.replace(o, b'oe')
    string = string.replace(O, b'Oe')
    string = string.replace(ss, b'ss')

    string = string.decode('utf-8')
    return string
    
def replace_multiple_underscores(string):
    '''
    if more then one underscore, reduce it to just one underscore
    '''
    return re.sub(r'_+', '_', string) 

def remove_begin_and_end_underscores(string):
    '''
    remove trailing underscore
    '''
    return string.rstrip('_').lstrip('_')

def create_file_name(tiddler_title):
    '''
    cleans tiddler title, only allows letters and numbers as file name, set underscores, etc
    expand it to your own cleaning needs
    '''
    file_name = clean_string(tiddler_title)
    file_name = file_name.lower()
    file_name = file_name.strip()
    file_name = re.sub(r'[^a-zA-Z0-9]', '_', file_name)
    file_name = replace_multiple_underscores(file_name)
    file_name = remove_begin_and_end_underscores(file_name)
    
    file_name= file_name[:maximum_file_name_length] # maximum letters for the file name
    return file_name

def create_text_content(tiddler,exportet_file_tiddler_contents):
    '''
    creates text content, based of the configured fields, that should be included in the final text
    change this function if you want to rearrange the text content
    returns a string of the extracted content
    '''
    result = []
    for key, value in tiddler.items():
        if key in exportet_file_tiddler_contents:
            result.append(value)
    return "\n\n".join(result) # return string


# Application start
# open local tiddlywiki file
with open(tiddly_wiki_file, 'r', encoding='utf-8') as file:
    content = file.read()

# create soup object
soup = BeautifulSoup(content, 'html.parser')

# select only the tiddlywiki-tiddler-store tag 
script_tag = soup.find('script', {'class': 'tiddlywiki-tiddler-store', 'type': 'application/json'})

tiddler_store_data = json.loads(script_tag.string) # parse soup object into dictionary

# iterate through tiddler data
for tiddler_data in tiddler_store_data:
    
    title = tiddler_data.get("title").strip()

    if not "$:" in title: # only process text data tiddlers, no system/template tiddlers, 
        type = tiddler_data.get("type")
        if type in ignore_types: # exclude tiddlers based on type
            continue

        # create file name
        file_name = create_file_name(title)#clean_string(title)

        # create file content
        text_content = create_text_content(tiddler_data, exportet_file_tiddler_contents)

        # create export folder, if it doesnt exist
        os.makedirs(export_directory, exist_ok=True)


        # create full file path to export folder
        file_path = os.path.join(export_directory, f'{file_name}.{exportet_file_extension}')

        with open(file_path, 'w', encoding='utf-8') as file: # write text content to file
            file.write(text_content)

        # set file creation and modified date to tiddlers created and modified
        created = tiddler_data.get("created")
        modified = tiddler_data.get("modified")
        new_creation_time = datetime.strptime(created, '%Y%m%d%H%M%S%f').timestamp()
        new_modified_time = datetime.strptime(modified, '%Y%m%d%H%M%S%f').timestamp()
        os.utime(file_path, (new_creation_time, new_modified_time))

