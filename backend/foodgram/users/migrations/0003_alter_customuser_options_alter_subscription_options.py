# Generated by Django 4.2.4 on 2023-08-10 14:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_subscription_subscription_unique_author_subscriber"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={
                "verbose_name": "пользователь",
                "verbose_name_plural": "пользователи",
            },
        ),
        migrations.AlterModelOptions(
            name="subscription",
            options={"verbose_name": "подписка", "verbose_name_plural": "подписки"},
        ),
    ]
