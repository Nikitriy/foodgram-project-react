from rest_framework import serializers

from recipes.models import *


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='ingredient.id', queryset=Ingredient.objects.all())
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(many=True, source='recipe_ingredient')

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'cooking_time', 'ingredients', 'tags')
        read_only_fields = ('id', 'author')


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='ingredient.id', queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientCreateSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'image', 'text', 'cooking_time', 'ingredients', 'tags')
    
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance = super().create(validated_data)
        recipes = []
        for ingredient_data in ingredients:
            recipes.append(RecipeIngredient(
                recipe=instance,
                ingredient=ingredient_data['ingredient'],
                amount=ingredient_data['amount'],
            ))
        RecipeIngredient.objects.bulk_create(recipes)
        return super().create(validated_data)


class RecipeSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
