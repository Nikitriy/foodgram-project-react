# Generated by Django 4.2.4 on 2023-08-13 13:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Favorite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "избранное",
                "verbose_name_plural": "избранное",
            },
        ),
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="название")),
                (
                    "measurement_unit",
                    models.CharField(max_length=200, verbose_name="единица измерения"),
                ),
            ],
            options={
                "verbose_name": "ингредиент",
                "verbose_name_plural": "ингредиенты",
            },
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="название")),
                ("image", models.ImageField(upload_to="", verbose_name="картинка")),
                ("text", models.TextField(verbose_name="описание")),
                (
                    "cooking_time",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="время приготовления",
                    ),
                ),
            ],
            options={
                "verbose_name": "рецепт",
                "verbose_name_plural": "рецепты",
                "ordering": ["-pk"],
            },
        ),
        migrations.CreateModel(
            name="RecipeIngredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="тег")),
                ("color", models.CharField(max_length=7, verbose_name="цвет")),
                (
                    "slug",
                    models.SlugField(max_length=200, unique=True, verbose_name="слаг"),
                ),
            ],
            options={
                "verbose_name": "тег",
                "verbose_name_plural": "теги",
            },
        ),
        migrations.CreateModel(
            name="ShoppingCart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shopping_cart_users",
                        to="recipes.recipe",
                        verbose_name="рецепт",
                    ),
                ),
            ],
            options={
                "verbose_name": "список покупок",
                "verbose_name_plural": "списки покупок",
            },
        ),
    ]
