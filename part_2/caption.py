import requests as r 
from requests.exceptions import HTTPError
import os
import zipfile
import json as j
from string import punctuation
import json

def get_folders_of_pictures(directory, file_name):
    """unzips files storing images into a folder with same name.
    directory string
    zip_name string"""
    with zipfile.ZipFile(f'{directory}/pictures/{file_name}.zip','r') as zip_ref:
        zip_ref.extractall(file_name)

def read_through_folders(folder):
    """reads images in the given folder and returns a list of captions.
    folder_names list"""
    captions = []
    for file_name in os.listdir(folder):
        # only read .png files
        if file_name.endswith('.png'):
            # track the process
            print(f'processing: {folder}/{file_name}')
            img_caption = {"img_path": f'{folder}/{file_name}'}
            captions_lst = get_captions(f'{folder}/{file_name}')
            try:    # to avoid nontype produced by failed requests 
                img_caption["caption"] = '; '.join(captions_lst)
            except:
                print('An error happened!')  
                img_caption["caption"]  = "No caption generated"
            captions.append(img_caption) 
    return captions  

def get_captions(img_path):
    """generates captions based on given image, by using Image Captioning REST 
    API.
    img_path string"""
    # upload images into the api and get captions back
    try:
        data = open(img_path, 'rb').read()
        response = r.post('http://localhost:8764/inception/v3/caption/image', data=data)
        response.raise_for_status()
        # access into returned json 
        response_json = response.json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        all_captions = set()
        for caption in response_json['captions']:
            # remove punctuations and space around captions and avoid
            # the duplicate captions
            caption_sentence = caption['sentence'].strip(' ').strip(punctuation).strip(' ')
            all_captions.add(caption_sentence)
        return list(all_captions)

def main():
    current_directory = os.getcwd()
    # image folders that we will need:
    lst_folder_names = ['Reconnaissance-800_result', 'Social_Engineering-800_result', 'Malware-800_result', 'Credential_Phishing-800_result']
    # unzip files storing images to folders with same names 
    for folder_name in lst_folder_names:
        get_folders_of_pictures(current_directory, folder_name)
        # read images in folders and generates the list of captions for them 
        captions = read_through_folders(folder_name)
        # writes the results into a txt file 
        with open(f'{folder_name}.json', 'w') as json_file:
            json.dump(captions, json_file)
    
if __name__ == "__main__":
    main()