from rest_framework import serializers

from recipes.models import *

class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='name')

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'description', 'cooking_time', 'ingredients', 'tags')
        read_only_fields = ('id', 'author')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'quality', 'unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
