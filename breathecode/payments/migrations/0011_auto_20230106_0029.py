# Generated by Django 3.2.16 on 2023-01-06 00:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0010_asyncconsumable'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumptionSession',
            fields=[
                ('id',
                 models.BigAutoField(auto_created=True, primary_key=True, serialize=False,
                                     verbose_name='ID')),
                ('eta', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('how_many', models.FloatField(default=0)),
                ('status',
                 models.CharField(choices=[('PENDING', 'Pending'), ('DONE', 'Done'),
                                           ('CANCELLED', 'Cancelled')],
                                  default='PENDING',
                                  max_length=12)),
                ('was_discounted', models.BooleanField(default=False)),
                ('request', models.JSONField()),
                ('path', models.CharField(blank=True, max_length=200)),
                ('related_id', models.IntegerField(blank=True, default=None, max_length=200, null=True)),
                ('related_slug', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('consumable',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.consumable')),
                ('user',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(name='AsyncConsumable', ),
    ]
