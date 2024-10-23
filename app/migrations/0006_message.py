# Generated by Django 4.2.16 on 2024-10-23 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0005_order_remove_favorite_product_remove_favorite_user_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("text", models.TextField()),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages_received",
                        to="app.user",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages_sent",
                        to="app.user",
                    ),
                ),
            ],
        ),
    ]