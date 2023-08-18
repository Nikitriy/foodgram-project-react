from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.serializers import CustomUserSerializer

MIN_VALUE = 1
MAX_VALUE = 32000


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source="ingredient.id", queryset=Ingredient.objects.all()
    )
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    image = Base64ImageField()
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(
        many=True, source="recipe_ingredient"
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        read_only_fields = (
            "id",
            "author",
            "is_favorited",
            "is_in_shopping_cart",
        )

    def get_is_favorited(self, obj):
        return obj.favorite_users.exists()

    def get_is_in_shopping_cart(self, obj):
        return obj.shopping_cart_users.exists()


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=MIN_VALUE, max_value=MAX_VALUE)

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount")


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = RecipeIngredientCreateSerializer(many=True)
    is_favorited = serializers.ReadOnlyField(default=False)
    is_in_shopping_cart = serializers.ReadOnlyField(default=False)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    cooking_time = serializers.IntegerField(
        min_value=MIN_VALUE, max_value=MAX_VALUE
    )

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def recipe_ingredient_create(self, recipe, ingredients):
        recipes = []
        for ingredient_data in ingredients:
            recipes.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient_data.get("id"),
                    amount=ingredient_data.get("amount"),
                )
            )
        RecipeIngredient.objects.bulk_create(recipes)

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        instance = super().create(validated_data)
        instance.tags.set(tags)
        self.recipe_ingredient_create(instance, ingredients)
        return instance

    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        RecipeIngredient.objects.filter(recipe=instance).delete()
        instance.tags.clear()
        instance.ingredients.clear()
        instance = super().update(instance, validated_data)
        instance.tags.set(tags)
        self.recipe_ingredient_create(instance, ingredients)
        return instance

    def to_representation(self, recipe):
        return RecipeSerializer(recipe).data
