from lib2to3.pgen2 import token
import os
import requests
import time 
import PySimpleGUI as sg
from pprint import pprint
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

    # Get ID method of VK user with digits check.
    def get_ID_VK():
        """It is the get ID method of VK user with digits checking."""
        while True:
            owner_id = input('Please, input the ID VK user (attention: only digits!): ')
            if owner_id.isdigit():
                print(f'OK, recieved ID {owner_id} from you.')
                break
            print(f"You write {owner_id}. It's wrong ID!")                 
        return owner_id

    # Check user ID function in base of VK. 
    def check_ID_VK():
        """It is the function check user ID in base of VK."""
        token = VkGetPhoto.token_VK()
        url = 'https://api.vk.com/method/users.get'
        params = {
            'user_id': VkGetPhoto.get_ID_VK(),
            'access_token': token, 
            'v':'5.131'
        }
        res_search = requests.get(url=url, params=params)
        if res_search.json()['response'] == []:
            text_check_result = f'This ID user is not really existing!'
        else:
            search_ID = res_search.json()['response'][0]['id']
            first_name_ID = res_search.json()['response'][0]['first_name']
            last_name_ID = res_search.json()['response'][0]['last_name']
            text_check_result = f'ID user {search_ID} is real existing!\nFirst name is: {first_name_ID}.\nLast name is: {last_name_ID}.'
        print(text_check_result)

    def my_function_VK_3():
        """It is a docstring"""
        return None

    def my_function_VK_4():
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


VkGetPhoto.check_ID_VK()