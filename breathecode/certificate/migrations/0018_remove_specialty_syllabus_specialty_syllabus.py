# Generated by Django 5.1.7 on 2025-03-22 17:35

from django.db import migrations, models


def migrate_syllabus(apps, schema_editor):
    Specialty = apps.get_model("admissions", "Specialty")
    Syllabus = apps.get_model("admissions", "Syllabus")

    for specialty in Specialty.objects.all():
        syllabus = Syllabus.objects.filter(id=specialty.id).first()
        if syllabus:
            specialty.syllabus.add(syllabus)


class Migration(migrations.Migration):

    dependencies = [
        ("certificate", "0017_layoutdesign_foot_note"),
        ("admissions", "0068_merge_20241216_1552"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="specialty",
            name="syllabus",
        ),
        migrations.AddField(
            model_name="specialty",
            name="syllabus",
            field=models.ManyToManyField(
                blank=True, help_text="This specialty can have multiple certificates", to="admissions.syllabus"
            ),
        ),
        migrations.RunPython(migrate_syllabus),
    ]
