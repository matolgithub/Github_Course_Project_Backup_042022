import os
import requests
import time 
import PySimpleGUI as sg
from pprint import pprint
# Не забыть в конце курсовой работы проверить и внести в requirements.txt все библиотеки и фреймворки!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class VkGetPhoto:
    def __init__(self, token_vk: str):
        self.token_vk = token_vk

    def my_function_VK_1():
        """It is a docstring"""
        return None

    def my_function_VK_2():
        """It is a docstring"""
        return None

    def my_function_VK_3():
        """It is a docstring"""
        return None

class YandexUploader(VkGetPhoto):
    def __init__(self, token_vk: str, token_ya: str):
        super().__init__(token_vk)
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

progress_bar()