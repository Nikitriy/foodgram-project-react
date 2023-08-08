from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()

class Recipe(models.Model):
    author = models.ForeignKey(User, related_name='recipes', on_delete=models.CASCADE, verbose_name='автор')
    name = models.CharField(max_length=200, verbose_name='название')
    image = models.ImageField(verbose_name='картинка')
    text = models.TextField(verbose_name='описание')
    cooking_time = models.PositiveIntegerField(validators=[MinValueValidator(1),], verbose_name='время приготовления')
    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient', verbose_name='ингредиенты')
    tags = models.ManyToManyField('Tag', verbose_name='теги')

    class Meta:
        ordering = ['-pk',]
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='название')
    measurement_unit = models.CharField(max_length=200, verbose_name='единица измерения')

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='тег')
    color = models.CharField(max_length=7, verbose_name='цвет')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='слаг')

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self) -> str:
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients', verbose_name='рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recipe_ingredients', verbose_name='ингредиент')
    amount = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'{self.recipe} - {self.ingredient}'
