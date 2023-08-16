from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import CustomUser

MIN_VALUE = 1
MAX_VALUE = 32000


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        related_name='all_recipes',
        on_delete=models.CASCADE,
        verbose_name='автор',
    )
    name = models.CharField(max_length=200, verbose_name='название')
    image = models.ImageField(verbose_name='картинка')
    text = models.TextField(verbose_name='описание')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_VALUE),
            MaxValueValidator(MAX_VALUE),
        ],
        verbose_name='время приготовления',
    )
    ingredients = models.ManyToManyField(
        'Ingredient', through='RecipeIngredient', verbose_name='ингредиенты'
    )
    tags = models.ManyToManyField('Tag', verbose_name='теги')

    class Meta:
        ordering = [
            '-pk',
        ]
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='название')
    measurement_unit = models.CharField(
        max_length=200, verbose_name='единица измерения'
    )

    class Meta:
        ordering = [
            '-pk',
        ]
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='тег')
    color = models.CharField(max_length=7, verbose_name='цвет')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='слаг')

    class Meta:
        ordering = [
            '-pk',
        ]
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self) -> str:
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_VALUE),
            MaxValueValidator(MAX_VALUE),
        ],
        verbose_name='количество',
    )

    class Meta:
        ordering = [
            '-pk',
        ]

    def __str__(self) -> str:
        return f'{self.recipe} - {self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_users',
        verbose_name='рецепт',
    )

    class Meta:
        ordering = [
            '-pk',
        ]
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_cart_recipes',
        verbose_name='пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart_users',
        verbose_name='рецепт',
    )

    class Meta:
        ordering = [
            '-pk',
        ]
        verbose_name = 'список покупок'
        verbose_name_plural = 'списки покупок'

    def __str__(self):
        return f'{self.user} - {self.recipe}'
