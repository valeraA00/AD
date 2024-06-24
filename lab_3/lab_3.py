import os
import datetime
import pandas as pd
import seaborn as sns
import urllib.request
from spyre import server
import matplotlib.pyplot as plt

############# Функції з лаби 2 ###############

def download_data(province_ID, start_year=1981, end_year=2024):
    # перевіряю, чи існує папка для зберігання
    if not os.path.exists("lab2_VHI"):
        os.makedirs("lab2_VHI")
    
    # перевіряю, чи файл уже завантажений
    filename_pattern = f"VHI-ID_{province_ID}_"
    existing_files = [file for file in os.listdir("lab2_VHI") if file.startswith(filename_pattern)]
    if existing_files:
        print(f"=] Файл для VHI-ID №{province_ID} вже існує: {existing_files[0]}\n")
        return
    

