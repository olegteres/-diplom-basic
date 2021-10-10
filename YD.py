import requests
import json
import os
from datetime import datetime


class YandexDisk:
    def __init__(self, token, json_path, user_folder):
        self.token = token
        self.json_path = json_path
        self.user_folder = user_folder

    def _get_data_by_json(self):
        data = dict()
        path = os.path.join(self.json_path, self.user_folder)

        if not os.path.exists(path):
            return False

        json_files_list = os.listdir(path)

        for json_file in json_files_list:
            json_file_path = os.path.join(path, json_file)

            if not os.path.isdir(json_file_path):
                if not os.path.exists(json_file_path):
                    return False

                with open(json_file_path) as f:
                    data = json.load(f)
        return data

    def _get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {self.token}"
        }

    def mkdir(self, folders: list):
        headers = self._get_headers()
        url = "https://cloud-api.yandex.net/v1/disk/resources"

        root_dir = ""

        for index, folder in enumerate(folders):
            if index == 0:
                params = {
                    "path": folder
                }

                response = requests.put(url, headers=headers, params=params, timeout=5)
                root_dir += f"{folder}/"

                if response.status_code == 201:
                    f_str = f"Создана корневая папка {folder}"
                    print(f_str)
            else:
                root_dir += f"{folders[index]}/"
                params = {
                    "path": root_dir
                }

                response = requests.put(url, headers=headers, params=params)

                if response.status_code == 201:
                    f_str = f"Создана папка {folder} по пути {root_dir}"
                    print(f_str)

        return root_dir

    def upload(self):
        data = self._get_data_by_json()

        if not data:
            print("Нет файлов для загрузки")
            return

        results = data["results"]
        first_name = data['first_name']
        last_name = data['last_name']
        id_ = data['id']
        user_name = data['user_name']

        headers = self._get_headers()
        root_path = self.mkdir(["VK", f"{user_name}-{first_name} {last_name}-{id_}"])
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload/"

        for item in results:
            url_path = results[item]["photo_url"]
            file_name = item

            params = {
                "path": f"{root_path}{file_name}",
                "url": url_path
            }

            response = requests.post(url=url, headers=headers, params=params, timeout=5)

            if response.status_code == 202:
                print(f"Загрузка файла {file_name} произошла успешно")
        print("Загрузка всех файлов завершена")

        # Перемещение файлов в папку резервного копирования
        base_url = os.path.join(self.json_path, self.user_folder)
        backup_path = os.path.join(base_url, "backup")
        date_backup = datetime.now().strftime("%m-%d-%Y %H%M%S")

        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
            os.rename(f"{base_url}\\{user_name}-{first_name} {last_name}-{id_}.json",
                      f"{backup_path}\\{user_name}-{first_name} {last_name}-{id_}_{date_backup}.json")
        else:
            os.rename(f"{base_url}\\{user_name}-{first_name} {last_name}-{id_}.json",
                      f"{backup_path}\\{user_name}-{first_name} {last_name}-{id_}_{date_backup}.json")