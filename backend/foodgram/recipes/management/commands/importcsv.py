import csv
import os

from django.core.management.base import BaseCommand
from foodgram.settings import BASE_DIR
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка данных из CSV файлов в Django ORM'

    def handle(self, *args, **options):
        file_path = os.path.join(BASE_DIR, 'data')
        with open(
            f'{file_path}/ingredients.csv', 'r', encoding='UTF-8'
        ) as file:
            for ingredient in csv.reader(file):
                Ingredient.objects.get_or_create(
                    name=ingredient[0], measurement_unit=ingredient[1]
                )
