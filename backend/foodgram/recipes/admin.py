from django.contrib import admin
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)


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
        'tags',
        'image',
        'text',
        'cooking_time',
        'ingredients',
        'favorite',
    )
    list_filter = ('author', 'name', 'tags')

    def favorite(self, obj):
        return obj.favorite_users.count()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field == 'ingredients':
            kwargs['queryset'] = Ingredient.objects.filter(
                recipe_ingredients__recipe=self.get_object()
            )
        if db_field == 'tags':
            kwargs['queryset'] = Tag.objects.filter(
                recipe_set=self.get_object()
            )
        return super().formfield_for_manytomany(db_field, request, **kwargs)
