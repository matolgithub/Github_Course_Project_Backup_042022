import os
import requests
import time 
import json
import PySimpleGUI as sg
from pprint import pprint
from datetime import date, datetime
# Не забыть в конце курсовой работы проверить и внести в requirements.txt все библиотеки и фреймворки!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class VkGetPhoto:
    # ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
    def __init__(self, token: str):
        self.token = token

    # Token VK function. 
    def token_VK():
        """It is the token function for the access to VK."""
        with open('token.txt', 'r') as file:
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
                break
        return max_photos_dict

    # Rename filename function for the files with same numbers of likes.
    def same_likes_func():
        """It is rename file name method for the files with same numbers of likes."""
        new_name_dict = VkGetPhoto.selection_get_photos()
        while True:
            for i, j in new_name_dict.items():
                for k, l in new_name_dict.items():
                    if j['file_name'] == l['file_name'] and i != k:
                        j['file_name'] = str(str(j['likes']) + '_likes' + ':' + j['date'] + '.jpg')
                        l['file_name'] = str(str(j['likes']) + '_likes' + ':' + j['date'] + '.jpg')
            break
        return new_name_dict    

    # Creating json-file function.
    def json_create():
        """This is creating json-file function."""
        data_dict = VkGetPhoto.same_likes_func()
        data_json = []
        for i in data_dict.values():
            list_json_item = {}
            list_json_item['file_name'] = i['file_name']
            list_json_item['size'] = i['max_photo_type']
            data_json.append(list_json_item)
        with open("file_photos.json", "w") as write_file:
            json.dump(data_json, write_file)
        print("The json file with photos info successfully created!")
        pprint(data_json)

class YandexUploader:
    def __init__(self, token_ya: str):
        self.token_ya = token_ya
    
    def my_function_YA_1():
        """It is a docstring"""
        return None

    def my_function_YA_2():
        """It is a docstring"""
        return None

    def my_function_YA_3():
        """It is a docstring"""
        return None

# Не забыть включить в блок выполнения программы прогресс-бар!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def progress_bar():
    """It is the indicator function to visualize the process of program execution."""
    mylist = [1,2,3,4,5,6,7,8]
    for i, item in enumerate(mylist):
        sg.one_line_progress_meter('Progress bar.', i+1, len(mylist), 'It is indicator of progress.', orientation='h', bar_color='red', no_titlebar=True, size=(60,10), no_button=True)
        time.sleep(1)


# testing part:
# VkGetPhoto.get_photos_VK() - successfully
# print(VkGetPhoto.convert_date(1562944607)) - successfully
# VkGetPhoto.dict_list_photos_VK(10)  - successfully
# VkGetPhoto.selection_get_photos()  - successfully
# VkGetPhoto.same_likes_func()  - successfully
VkGetPhoto.json_create()