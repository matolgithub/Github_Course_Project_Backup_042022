from hashlib import md5
import os
from sys import api_version
from urllib.error import HTTPError
from webbrowser import get
import requests
import time 
import json
import PySimpleGUI as sg
from pprint import pprint
from datetime import date, datetime
import urllib.request
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from apiclient import errors
from apiclient import http
import io
import pickle
import os.path
import shutil
from mimetypes import MimeTypes
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from ok_api import OkApi

# Не забыть в конце курсовой работы проверить и внести в requirements.txt все библиотеки и фреймворки!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Main form function
def main_form():
    """It is main form function"""
    window = Tk()
    window["bg"] = "black"
    window.title("Python - choice user form.")
    input_label_ID = Label(text="Please, make a choice what are you going to do:", fg='white', bg='black')
    input_label_ID.grid(row=1, column=1, sticky="w")
    VK_YD_button = Button(text="From VK to Yandex Disk ", activebackground='red', highlightcolor='red', bg='blue', fg='white', command=VkGetPhoto.VK_YD_from_but)
    VK_GD_button = Button(text="From VK to Google Drive", activebackground='red', highlightcolor='red', bg='blue', fg='white', command=GoogleDriveUploader.upload_gd_files)
    GD_YD_button = Button(text="From GD to Yandex Disk", activebackground='red', highlightcolor='red', bg='blue', fg='white', command=GoogleDriveUploader.get_gd_files)
    Ok_YD_button = Button(text="From Ok to Yandex Disk  ", activebackground='red', highlightcolor='red', bg='blue', fg='white', command=OkGetPhoto.download_ok)
    close_button = Button(text="Close form", activebackground='red', highlightcolor='red', bg='blue', fg='white', command=exit)
    VK_YD_button.grid(row=3, column=1, padx=10, pady=10, sticky="e")
    VK_GD_button.grid(row=4, column=1, padx=10, pady=10, sticky="e")
    GD_YD_button.grid(row=5, column=1, padx=10, pady=10, sticky="e")
    Ok_YD_button.grid(row=6, column=1, padx=10, pady=10, sticky="e")
    close_button.grid(row=7, column=3, padx=10, pady=10, sticky="e")
    window.mainloop()


# Result form function
def result_form():
    """It is result form function"""
    messagebox.showinfo('It is result form', 'Process is complete!')


class VkGetPhoto:
    def __init__(self, token: str):
        self.token = token

    # Token VK function. 
    def token_VK():
        """It is the token function for the access to VK."""
        with open('token_VK.txt', 'r') as file:
            token = file.read().strip()    
        return token

    # Get ID method of VK user with digits check and VK base check.
    def get_ID_VK():
        """It is the get ID method of VK user with digits and VK base checking."""
        while True:
            owner_id = input('Please, input the ID VK user (attention: only digits!): ')
            if owner_id.isdigit():
                token = VkGetPhoto.token_VK()
                url = 'https://api.vk.com/method/users.get'
                params = {
                    'user_id': owner_id,
                    'access_token': token, 
                    'v':'5.131'
                }
                res_search = requests.get(url=url, params=params)
                if res_search.json()['response'] == []:
                    print(f'You write {owner_id}. This ID user is not really existing! Try again!')
                else:
                    search_ID = res_search.json()['response'][0]['id']
                    first_name_ID = res_search.json()['response'][0]['first_name']
                    last_name_ID = res_search.json()['response'][0]['last_name']
                    print(f'ID user {search_ID} is real existing!\nFirst name is: {first_name_ID}.\nLast name is: {last_name_ID}.')
                    break         
        return owner_id

    # Function for the getting profile photos by ID user and type/number albums. 
    def get_photos_VK(num_count):
        """This is function to get profile photos by ID user and type/number albums."""
        while True:
            choice_album = input('Please, input type album ("profile" or "wall") or give ID of album: ')
            if choice_album == "profile" or choice_album == "wall" or choice_album.isdigit():
                break
            else:
                print("Wrong input, try again!")
        token = VkGetPhoto.token_VK()
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': VkGetPhoto.get_ID_VK(),
            'access_token': token, 
            'v':'5.131',
            'album_id' : choice_album,
            'extended' : '1',
            'photo_sizes' : '1',
            'count' : num_count
        }
        res_get_photos = requests.get(url=url, params=params)
        try:
            get_album_photos = res_get_photos.json()['response']['items']
        except KeyError:
            print(f"Sorry! Have a problem to get photos from {choice_album} for this ID user.")
        return get_album_photos

    # Function converting date from sec to day-month-year.
    def convert_date(date_sec):
        """This method for converting date from sec to day-month-year."""
        norm_date = datetime.fromtimestamp(date_sec).strftime("%d_%B_%Y")
        return norm_date  

    # Function to create list and dictionary of getting photos from the user ID account.
    def dict_list_photos_VK(num_photos=5):
        """This is the method creating list and dictionary for getting photos from the user ID account."""
        dict_id_photos = {}
        while True:
            list_id_photos = []
            count_photos = 0
            try:
                all_photos = VkGetPhoto.get_photos_VK(num_photos)
                for item in all_photos:
                    list_id_photos.append(item['id'])
                    list_id_photos = list_id_photos[::-1]       # sorted from newest to oldest
                    count_photos += 1
            except UnboundLocalError:
                print(f'It is not possible to create list photos for this user. Maybe it is closed or deleted profile.')
                break
            else:
                list_id_photos = list_id_photos[:num_photos]
                print(f'The user have {count_photos} photos. You requested {num_photos}. The list of photos is: {list_id_photos}.')
                break
        for i in list_id_photos:
            for j in all_photos:
                if j['id'] == i:
                    dict_id_photos[i] = j
        return dict_id_photos

    # Function for the selection getting photos from the user ID account with the maximum sizes.
    def selection_get_photos():
        """It is the method for the selection getting photos from the user ID account with the maximum sizes."""
        max_photos_dict = {}
        list_VK_type = ['w', 'z', 'y', 'x', 'r', 'q','p','o', 'm', 's']
        while True:
            inp_num_photos = input('Input the numbers of photos you need (by default "5"): ')
            try:
                result_photos = VkGetPhoto.dict_list_photos_VK(int(inp_num_photos))
            except ValueError:
                print('Wrong, try again!')
            else:
                for i in result_photos:
                    max_perim = 0
                    type_max_photo = ''
                    if result_photos[i]['sizes'] != []:
                        for j in result_photos[i]['sizes']:
                            if j['height'] == 0 and j['width'] == 0:
                                for type_photo in list_VK_type:
                                    if j['type'] == type_photo:
                                        type_max_photo = type_photo
                                        max_perim = (int(j['height']) + int(j['width']))
                                        likes_count = result_photos[i]['likes']['count']
                                        break
                            else:
                                half_perim = (int(j['height']) + int(j['width']))
                                if half_perim > max_perim:
                                    max_perim = half_perim
                                    type_max_photo = j['type']
                            likes_count = result_photos[i]['likes']['count']
                            max_photos_dict[i] = {
                                'url' : j['url'],    
                                'max_half_perim' : max_perim,
                                'max_photo_type' : type_max_photo,
                                'date' : VkGetPhoto.convert_date(result_photos[i]['date']),
                                'likes' : likes_count,
                                'file_name' : f'{likes_count}.jpg'
                            }
                    else:
                        print("List 'sizes' is empty.")     
                break  
        return max_photos_dict

    # Rename filename function for the files with same numbers of likes.
    def same_likes_func():
        """It is rename file name method for the files with same numbers of likes."""
        new_name_dict = VkGetPhoto.selection_get_photos()
        while True:
            for i, j in new_name_dict.items():
                count_same = 0
                for k, l in new_name_dict.items():
                    if j['file_name'] == l['file_name'] and i != k:
                        count_same += 1
                        j['file_name'] = str(str(j['likes']) + '_likes' + f"_{count_same}" + '-' + j['date'] + '.jpg')
                        count_same += 1
                        l['file_name'] = str(str(j['likes']) + '_likes' + f"_{count_same}" + '-' + j['date'] + '.jpg')
            break
        return new_name_dict    

    # Copy files from VK and create json file - function.
    def copy_photos(name_folder):
        """This is copy files from VK and create json file - function."""
        count_files = 0
        count_percent = 0
        copy_photos = VkGetPhoto.same_likes_func()
        VkGetPhoto.json_create(copy_photos)
        if not os.path.isdir(name_folder):
            os.mkdir(name_folder)
        os.chdir(name_folder)
        time_start = datetime.now()
        for i in copy_photos.values():
            url = i['url']
            try:
                urllib.request.urlretrieve(url, str(i["file_name"]))
            except HTTPError:
                print('Terribly sorry, but there is HTTP problem!')
            else:        
                count_files += 1
                count_percent += round((100 / len(copy_photos)), 1)
                print("#" *  int(count_percent/5), f'{count_percent}%', end='')
        time_end = datetime.now()  
        period = time_end - time_start
        print(f" The copying photos from VK successfully complete in {name_folder}! Start: {time_start}, end: {time_end}, total run time: {period}.")

    # Creating json-file function.
    def json_create(data_dict):
        """This is creating json-file function."""
        data_json = []
        for i in data_dict.values():
            list_json_item = {}
            list_json_item['file_name'] = i['file_name']
            list_json_item['size'] = i['max_photo_type']
            data_json.append(list_json_item)
        with open("file_photos.json", "w") as write_file:
            json.dump(data_json, write_file)
        print("The json file with photos info successfully created!")
        return data_json

    # Read json-file function.
    def read_json_file(file_name_json):
        """This is for reading json-file function."""
        with open(file_name_json, 'r', encoding='utf-8') as file:
            read_json = json.load(file)
        return read_json

    # Function copied files from VK to YD with push the button.
    def VK_YD_from_but(folder_name='VK_photos'):
        """It is function copied files from VK to YD with push the button."""
        VkGetPhoto.copy_photos(folder_name)
        os.chdir('..')
        YandexUploader(YandexUploader.token_Ya()).upload(folder_name)

class YandexUploader:
    def __init__(self, token_ya: str):
        self.token_ya = token_ya

    # Token Yandex Disk function. 
    def token_Ya():
        """It is the token function for the access to Yandex Disk."""
        with open('token_YaDisk.txt', 'r') as file:
            token_ya = file.read().strip()    
        return token_ya
    
    # Upload method photos getting from aplications move to Disk.Yandex
    def upload(self, folder_path='VK_photos'):
        """This is the upload method photos getting from aplications move to Disk.Yandex."""
        time_start = datetime.now()
        file_path = os.listdir(folder_path)
        count_files = 0
        count_percent = 0
        for i in file_path:
            upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
            headers = {'Content-Type' : 'application/json', 'Authorization' : f'OAuth {self.token_ya}'}
            params = {'path' : i, 'overwrite' : 'true'}
            response = requests.get(upload_url, params=params, headers=headers)
            href_json = response.json()
            data = {"file": open(f'{os.path.basename(folder_path)}/{i}', "rb")}
            response_upload = requests.post(url=href_json['href'], files=data)
            count_files += 1
            count_percent += round((100 / len(file_path)), 1)
            # print(f'The result of POST-operation is: "{response_upload.status_code}". Photo - {i} moved successfuly! File number: {count_files}; finished: {count_percent} percents.')
            print("*" *  int(count_percent/5), f'{count_percent}%', end='')
        time_end = datetime.now()
        period = time_end - time_start
        print(f' Copying files to Disk.Yandex - complete! Start: {time_start}, end: {time_end}, total run time: {period}.')
        result_form()
         

# ?????????????????????????????????????????????????????????????????????????????????????????????????????????? если убрать класс поплывут функции!
class GoogleDriveUploader:
    def __init__(self):
        pass

    def get_gd_files(file_id='1YOYIoJDzH6QDYQsMRXxb3PXgm-pxbKRE', file_name='5.jpg', name_folder='./Files_from_GD'):    
        SCOPES = ['https://www.googleapis.com/auth/drive']
        SERVICE_ACCOUNT_FILE = 'google_ser_key_py-52-060422.json'
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)
        request = service.files().get_media(fileId=file_id)
        new_f = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=new_f, request=request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print("Download in local folder complete successfully %d%%." % int(status.progress() * 100))
        new_f.seek(0)
        with open (os.path.join(name_folder, file_name), 'wb') as file:    
            file.write(new_f.read())
        YandexUploader.upload(YandexUploader(YandexUploader.token_Ya()), folder_path='Files_from_GD')
        

    def upload_gd_files(name_folder='VK_photos'):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        SERVICE_ACCOUNT_FILE = 'google_ser_key_py-52-060422.json'
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=credentials)

        folder_id = '1Bxn_CsWNLjvVAH60oDeBWr2NKpJoydCb'
        os.chdir(name_folder)
        files_in_dir = os.listdir()
        for i, files in enumerate(files_in_dir):
            sg.one_line_progress_meter('Progress bar.', i+1, len(files_in_dir), 'It is indicator of progress.', orientation='h', bar_color='red', no_titlebar=True, size=(60,10), no_button=True)
            name = files
            file_metadata = {'name': name, 'parents': [folder_id]}
            media = MediaFileUpload(files, resumable=True)
            id_res_upload = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            time.sleep(0.001)
            print(i + 1, f'file, ID: {id_res_upload}')
        print(f'Process is complete. To Google Drive copied files:', i + 1)
        result_form()


class OkGetPhoto:
    def __init__(self, session_key, application_key_ok, session_secret_key_ok ):
        self.session_key = session_key
        self.application_key_ok = application_key_ok
        self.session_secret_key_ok = session_secret_key_ok

    # Token function for access in Ok platform. 
    def session_key_ok():
        """It is session key function for access in Ok platform."""
        with open('session_key_ok.txt', 'r') as file:
            session_key = file.read().strip()    
        return session_key

    # Application key function for Ok.ru platform. 
    def application_key_Ok():
        """It is application key function for Ok.ru platform."""
        with open('application_key_ok.txt', 'r') as file:
            application_key_ok = file.read().strip()    
        return application_key_ok

    # Session secret key function for Ok.ru platform. 
    def session_secret_key_Ok():
        """It is session secret key function for Ok.ru platform."""
        with open('session_secret_key_ok.txt', 'r') as file:
            session_secret_key_ok = file.read().strip()    
        return session_secret_key_ok

    # Get photos from Ok.ru function.
    def get_photo_ok(aid='812270533647', count_photos=10):
        """It is get photos from Ok.ru function."""

        url = 'https://api.ok.ru/fb.do'
        str_param = ''
        params = {
            'application_key' : OkGetPhoto.application_key_Ok(),
            'aid' : aid,
            'count' : count_photos,
            'detectTotalCount' : True,
            'session_key' : OkGetPhoto.session_key_ok(),
            'sig' : '',
            'method' : 'photos.getPhotos'
        }     
        sorted_tuple = sorted(params.items(), key=lambda x: x[0])
        params = dict(sorted_tuple)
        for i in params:
            if i == 'sig':
                continue
            else:    
                str_param = str_param + i + '=' + str(params[i])
        str_param += OkGetPhoto.session_secret_key_Ok()
        sig = md5(str_param.encode()).hexdigest()
        params['sig'] = sig
        path = url
        for i in params:
            if i == 'aid':
                path = path + '?' + i + '=' + str(params[i])
            else:
                path = path + '&' + i + '=' + str(params[i])
        path = path + '&session_key' + '=' + OkGetPhoto.session_key_ok()
        response = requests.get(path).json()
        res_json = response['photos']
        # pprint(res_json)
        return res_json

    def download_ok(name_folder='Ok_photos'):
        count_files = 0
        count_percent = 0
        dict_ok_photos = {}
        dictok_photos = {}
        result_ok_dict = {}
        list_id_photos = []
        ok_photos = OkGetPhoto.get_photo_ok()
        if not os.path.isdir(name_folder):
            os.mkdir(name_folder)
        os.chdir(name_folder)
        time_start = datetime.now()
        for i in ok_photos: 
            list_id_photos.append(i['id'])
        for i in list_id_photos:
            list_ok_photos = []
            for j in ok_photos:
                for k in j:
                    if i == j['id'] and 'pic' in k:
                        list_ok_photos.append(k)
                dict_ok_photos[i] = list_ok_photos
        for  i, j in dict_ok_photos.items():
            dictok_photos[i] = j[-1]
        for i, j in dictok_photos.items():
            for k in ok_photos:
                if i == k['id']:
                    result_ok_dict[i] = k[j] 
        for id, url in result_ok_dict.items():
            file_name_ok = f'id{id}from_Ok.jpg'
            try:
                urllib.request.urlretrieve(url, filename=file_name_ok)
            except HTTPError:
                print('Terribly sorry, but there is HTTP problem!')
            else:        
                count_files += 1
                count_percent += round((100 / len(result_ok_dict)), 1)
                print("#" *  int(count_percent/5), f'{count_percent}%', end='')
        time_end = datetime.now()  
        period = time_end - time_start
        print(f" The copying photos from Ok successfully complete in local folder {name_folder}! Start time: {time_start}, end time: {time_end}. Total time: {period}.")
        os.chdir('..')
        YandexUploader.upload(YandexUploader(YandexUploader.token_Ya()), folder_path='Ok_photos')

if __name__ == '__main__':
    main_form()

    # testing part:
    # VkGetPhoto.get_photos_VK(5)- successfully
    # print(VkGetPhoto.convert_date(1562944607)) - successfully
    # VkGetPhoto.dict_list_photos_VK(10)  - successfully
    # VkGetPhoto.selection_get_photos()  - successfully
    # VkGetPhoto.same_likes_func()  - successfully
    # VkGetPhoto.json_create()  - successfully
    # VkGetPhoto.read_json_file('file_photos.json') - successfully
    # VkGetPhoto.copy_photos('VK_photos') - successfully
    # YandexUploader(YandexUploader.token_Ya()).upload('VK_photos') - successfully
    # GoogleDriveUploader.upload_gd_files() - successfully
    # GoogleDriveUploader.get_gd_files() - successfully