from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()

class Recipe(models.Model):
    author = models.ForeignKey(User, related_name='recipes', on_delete=models.CASCADE, verbose_name='автор')
    name = models.CharField(max_length=255, verbose_name='название')
    image = models.ImageField(verbose_name='картинка')
    description = models.TextField(verbose_name='описание')
    cooking_time = models.DurationField(verbose_name='время приготовления')
    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient', verbose_name='ингредиенты')
    tags = models.ManyToManyField('Tag', through='RecipeTag', verbose_name='теги')

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('recipe', kwargs={'pk': self.pk})


class Ingredient(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')
    quality = models.FloatField(verbose_name='количество')
    unit = models.CharField(max_length=255, verbose_name='единица измерения')

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('ingredient', kwargs={'pk': self.pk})


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='тег')
    color = models.CharField(max_length=16, verbose_name='цвет')
    slug = models.SlugField(verbose_name='слаг')

    def __str__(self) -> str:
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='ингредиент')

    def __str__(self) -> str:
        return f'{self.recipe} - {self.ingredient}'
