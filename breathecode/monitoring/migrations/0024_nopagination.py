# Generated by Django 5.1.2 on 2024-10-25 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monitoring", "0023_repositorysubscription_last_call"),
    ]

    operations = [
        migrations.CreateModel(
            name="NoPagination",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("path", models.CharField(max_length=255)),
                ("method", models.CharField(max_length=9)),
            ],
        ),
    ]
