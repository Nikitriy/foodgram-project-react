from django.contrib import admin

from recipes.models import *


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


admin.site.register(Ingredient)
admin.site.register(Tag)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
