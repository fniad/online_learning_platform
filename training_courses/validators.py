""" Валидаторы приложения training_courses """
import re

from rest_framework.serializers import ValidationError

from config import settings


class LinkValidator:
    """Проверка на ссылки в описании и url_видео"""

    def __init__(self, field):
        self.www_youtube_pattern = re.compile(
            r'((?:www\.)?youtube\.com|youtu.be)(.*)')
        self.http_youtube_pattern = re.compile(
            r'((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?'
        )
        self.app_domains = getattr(settings, 'ALLOWED_HOSTS', [])
        self.field = field

    def __call__(self, value):
        checked_fields = set()
        fields_to_check = ['video_url_lesson', 'description_lesson', 'description_course']
        field_errors = {}

        for field in fields_to_check:
            if field in checked_fields:
                continue

            checked_fields.add(field)
            field_value = value.get(field)

            if field_value is not None and not self.has_valid_links(field_value):
                field_errors[field] = ['Можно добавлять ссылки только на страницы этого сайта или youtube.com']

        if field_errors:
            raise ValidationError(field_errors)

    def has_valid_links(self, text):
        """ Проверка текстовых полей и поля ссылки на соответствие валидным паттернам """

        app_patterns_http, app_patterns_www = self.get_app_pattern()
        http_youtube_pattern = re.compile(self.http_youtube_pattern.pattern, re.UNICODE)
        www_youtube_pattern = re.compile(self.www_youtube_pattern.pattern, re.UNICODE)

        if ((http_youtube_pattern.search(text) or www_youtube_pattern.search(text)) and (app_patterns_http.search(
                text) or app_patterns_www.search(text))) or all(char.isalnum() or char.isspace() for char in text):
            return True

        return False

    def get_app_pattern(self):
        """ Генерация паттерна с доменами сайта"""
        app_patterns_http = []
        app_patterns_www = []
        if self.app_domains:
            for domain in self.app_domains:
                app_patterns_http.extend(self.get_app_http_patterns(domain))
                app_patterns_www.extend(self.get_app_www_patterns(domain))
        apps_pattern_http = '|'.join(app_patterns_http)
        apps_pattern_www = '|'.join(app_patterns_www)
        return re.compile(apps_pattern_http), re.compile(apps_pattern_www)

    @staticmethod
    def get_app_http_patterns(domain):
        """ Получение строки валидных символов для паттерна домена """
        return [
            rf'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:{re.escape(domain)}))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?'
        ]

    @staticmethod
    def get_app_www_patterns(domain):
        """ Получение строки валидных символов для паттерна домена """
        return [
            rf'((?:www\.)?{re.escape(domain)})(.*)'
        ]
