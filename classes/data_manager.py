import json

from classes.exceptions import DataSourceBrokenException


class DataManager:

    def __init__(self, path):
        self.path = path

    def _load_data(self):
        """ Загружает данные из файла для использования другими методами """
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):

            raise DataSourceBrokenException("Файл с данными повреждён")

        return data

    def _save_data(self, data):
        """ Перезаписывает переданные данные в файл с данными """
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def get_all(self):
        """ Отдаёт полный список данных """
        data = self._load_data()

        return data

    def search(self, substring):
        """ Отдаёт посты, которые содержат substring"""
        data = self._load_data()
        substring = substring.lower()

        matching_posts = [post for post in data if substring in post["content"].lower()]

        return matching_posts

    def add(self, post):
        """ Добавляет к постам определённый пост """
        if type(post) != dict:
            raise TypeError("Dict expected for adding post")

        posts = self._load_data()
        posts.append(post)
        self._save_data(posts)
