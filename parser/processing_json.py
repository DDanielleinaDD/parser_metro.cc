import os
import json


FOLDER_PATH = 'parser\\parcing result'


def make_file_path(document):
    file_path = os.path.join(FOLDER_PATH, document)
    return file_path


def save_result(response, document):
    file_path = make_file_path(document)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(response, file, ensure_ascii=False, indent=4)


def open_json(document):
    file_path = make_file_path(document)
    with open(file_path, 'r', encoding='utf-8') as file:
        products_data = json.load(file)['data']['category']['products']
        return products_data
