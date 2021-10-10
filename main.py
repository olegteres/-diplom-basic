from vk import VK
from ya_disk import YandexDisk
import os

VK_TOKEN = ...
Yandex_TOKEN = ...
username = ...
version = "5.131"
files_path = os.path.join(os.getcwd(), 'files')


v = VK(token=VK_TOKEN, user=username, version=version, count_to_upload=3)
v.collection_data()

ya = YandexDisk(token=Yandex_TOKEN, json_path=files_path, user_folder=username)
ya.upload()