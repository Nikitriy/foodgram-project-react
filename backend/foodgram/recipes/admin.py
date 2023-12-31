from django.contrib import admin
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = (
        'author',
        'name',
        'obtain_tags',
        'image',
        'text',
        'cooking_time',
        'obtain_ingredients',
        'favorite',
    )
    list_filter = ('author', 'name', 'tags')

    def favorite(self, obj):
        return obj.favorite_users.count()

    def obtain_tags(self, obj):
        return '\n'.join((tag.name for tag in obj.tags.all()))

    def obtain_ingredients(self, obj):
        return '\n'.join(
            (ingredient.name for ingredient in obj.ingredients.all())
        )
