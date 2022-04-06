import os
import requests
import time 
import json
import PySimpleGUI as sg
from pprint import pprint
from datetime import datetime
import urllib.request
# Не забыть в конце курсовой работы проверить и внести в requirements.txt все библиотеки и фреймворки!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


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
    def get_photos_VK():
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
            'count' : '1000'
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
                all_photos = VkGetPhoto.get_photos_VK()
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
                                        print(type_max_photo)
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
        for i in copy_photos.values():
            url = i['url']
            urllib.request.urlretrieve(url, str(i["file_name"]))
            count_files += 1
            count_percent += round((100 / len(copy_photos)), 1)
            print("#" *  int(count_percent/5), f'{count_percent}%', end='')
        print(f" The copying photos from VK successfully complete in {name_folder}!")

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

class YandexUploader:
    def __init__(self, token_ya: str):
        self.token_ya = token_ya

    # Token Yandex Disk function. 
    def token_Ya():
        """It is the token function for the access to Yandex Disk."""
        with open('token_YaDisk.txt', 'r') as file:
            token_ya = file.read().strip()    
        return token_ya

    def get_headers(self):  
        return {'Content-Type' : 'application/json', 'Authorization' : f'OAuth {self.token_ya}'}
    
    # Upload method photos getting from VK move to Disk.Yandex
    def upload(self, folder_path: str):
        """This is the upload method photos getting from VK move to Disk.Yandex."""
        file_path = os.listdir(folder_path)
        count_files = 0
        count_percent = 0
        for i in file_path:
            upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
            headers = self.get_headers()
            params = {'path' : i, 'overwrite' : 'true'}
            response = requests.get(upload_url, params=params, headers=headers)
            href_json = response.json()
            data = {"file": open(f'{os.path.basename(folder_path)}/{i}', "rb")}
            response_upload = requests.post(url=href_json['href'], files=data)
            count_files += 1
            count_percent += round((100 / len(file_path)), 1)
            # print(f'The result of POST-operation is: "{response_upload.status_code}". Photo - {i} moved successfuly! File number: {count_files}; finished: {count_percent} percents.')
            print("*" *  int(count_percent/5), f'{count_percent}%', end='')
        print(' Copying files to Disk.Yandex - complete!')
         
         
# Не забыть включить в блок выполнения программы прогресс-бар!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def progress_bar():
    """It is the indicator function to visualize the process of program execution."""
    mylist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for i, item in enumerate(mylist):
        sg.one_line_progress_meter('Progress bar.', i+1, len(mylist), 'It is indicator of progress.', orientation='h', bar_color='red', no_titlebar=True, size=(60,10), no_button=True)
        time.sleep(1)

if __name__ == '__main__':
    VkGetPhoto.copy_photos('VK_photos')
    os.chdir('..')
    YandexUploader(YandexUploader.token_Ya()).upload('VK_photos')


# testing part:
# VkGetPhoto.get_photos_VK() - successfully
# print(VkGetPhoto.convert_date(1562944607)) - successfully
# VkGetPhoto.dict_list_photos_VK(10)  - successfully
# VkGetPhoto.selection_get_photos()  - successfully
# VkGetPhoto.same_likes_func()  - successfully
# VkGetPhoto.json_create()  - successfully
# VkGetPhoto.read_json_file('file_photos.json') - successfully
# VkGetPhoto.copy_photos('VK_photos') - successfully
# YandexUploader(YandexUploader.token_Ya()).upload('VK_photos') - successfully