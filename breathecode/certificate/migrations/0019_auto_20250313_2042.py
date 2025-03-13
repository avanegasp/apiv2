# Generated by Django 5.1.6 on 2025-03-13 20:42

from django.db import migrations


def migrate_syllabus_data(apps, schema_editor):
    Specialty = apps.get_model("certificate", "Specialty")
    for specialty in Specialty.objects.all():
        if specialty.syllabus:
            specialty.syllabus_many.add(specialty.syllabus)


class Migration(migrations.Migration):

    dependencies = [
        ("certificate", "0018_specialty_syllabus_many"),
    ]

    operations = [
        migrations.RunPython(migrate_syllabus_data),
    ]
