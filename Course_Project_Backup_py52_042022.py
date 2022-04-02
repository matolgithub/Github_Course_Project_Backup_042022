import os
import requests
import time 
import PySimpleGUI as sg
from pprint import pprint
from datetime import datetime
# Не забыть в конце курсовой работы проверить и внести в requirements.txt все библиотеки и фреймворки!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class VkGetPhoto:
    def __init__(self, token_vk: str):
        self.token_vk = token_vk

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

    # Function for the getting profile photos by ID user. 
    def get_photos_VK():
        """This is function to get profile photos by ID user."""
        token = VkGetPhoto.token_VK()
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': VkGetPhoto.get_ID_VK(),
            'access_token': token, 
            'v':'5.131',
            'album_id' : 'profile',
            'extended' : '1',
            'photo_sizes' : '1',
            'count' : '100'
        }
        res_get_photos = requests.get(url=url, params=params)
        try:
            get_profile_photos = res_get_photos.json()['response']['items']
        except KeyError:
            print("Sorry! Different problems with this ID user!")
        else:
            pprint(get_profile_photos)
        return get_profile_photos

    # Function converting date from sec to day-month-year.
    def convert_date(date_sec):
        """This method for converting date from sec to day-month-year."""
        norm_date = datetime.fromtimestamp(date_sec).strftime("%d_%B_%Y")
        return norm_date  

    # Function to create list of ID getting profile photos from the user account.
    def profile_list_photos_VK(num_photos=5):
        """This is the method creating list of ID getting profile photos from the user account."""
        while True:
            list_id_photos = []
            count_photos = 0
            try:
                for item in VkGetPhoto.get_photos_VK():
                    list_id_photos.append(item['id'])
                    list_id_photos = list_id_photos[::-1]       # sorted from newest to oldest
                    count_photos += 1
            except UnboundLocalError:
                print(f'It is not possible to create list photos for this user. Maybe it is closed or deleted profile.')
                break
            else:
                if count_photos < num_photos:
                    print(f'The user have only {count_photos} profile photos. It is less, then you need.')
                elif count_photos == num_photos:
                    print(f'The user have {count_photos} profile photos. You need {num_photos} too.')
                elif count_photos > num_photos:
                    print(f'The user have {count_photos} profile photos. You need {num_photos} The part of photos not will be include in list.')
                list_id_photos = list_id_photos[:num_photos]
                print(f'The default value is 5 photos. You requested {num_photos}. The list of photos is: {list_id_photos}.')
                break
        return list_id_photos

    # Function for the selection getting profile photos from the user ID account with the maximum sizes.
    def selection_get_photos():
        """It is the method for the selection getting profile photos from the user ID account with the maximum sizes"""
        
        return None

    def my_function_VK_6():
        """It is a docstring"""
        return None    

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
# VkGetPhoto.profile_list_photos_VK(1500) - successfully