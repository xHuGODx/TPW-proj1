# Generated by Django 4.2.16 on 2024-11-01 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0009_user_admin"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="quantity",
        ),
    ]