from django.contrib import admin

from recipes.models import Ingredient, Recipe

admin.site.register(Recipe)
admin.site.register(Ingredient)
