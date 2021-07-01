# Generated by Django 3.0.8 on 2020-07-28 22:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('freelance', '0005_auto_20200717_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='reviewer',
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL),
        ),
    ]
