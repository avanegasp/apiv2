# Generated by Django 3.2.22 on 2023-10-17 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0034_assettechnology_is_deprecated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='asset_type',
            field=models.CharField(choices=[('PROJECT', 'Project'), ('EXERCISE', 'Exercise'),
                                            ('QUIZ', 'Quiz'), ('LESSON', 'Lesson'), ('VIDEO', 'Video'),
                                            ('ARTICLE', 'Article')],
                                   db_index=True,
                                   max_length=20),
        ),
        migrations.AlterField(
            model_name='asset',
            name='authors_username',
            field=models.CharField(blank=True,
                                   db_index=True,
                                   default=None,
                                   help_text='Github usernames separated by comma',
                                   max_length=80,
                                   null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='cleaning_status',
            field=models.CharField(
                blank=True,
                choices=[('PENDING', 'Pending'), ('ERROR', 'Error'), ('OK', 'Ok'), ('WARNING', 'Warning'),
                         ('NEEDS_RESYNC', 'Needs Resync')],
                db_index=True,
                default='PENDING',
                help_text='Internal state automatically set by the system based on cleanup',
                max_length=20,
                null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='external',
            field=models.BooleanField(
                db_index=True,
                default=False,
                help_text=
                'External assets will open in a new window, they are not built using breathecode or learnpack tecnology'
            ),
        ),
        migrations.AlterField(
            model_name='asset',
            name='github_commit_hash',
            field=models.CharField(blank=True, db_index=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='graded',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='asset',
            name='interactive',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='asset',
            name='is_seo_tracked',
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='lang',
            field=models.CharField(blank=True,
                                   db_index=True,
                                   default=None,
                                   help_text='E.g: en, es, it',
                                   max_length=2,
                                   null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='last_cleaning_at',
            field=models.DateTimeField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='last_seo_scan_at',
            field=models.DateTimeField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='last_synch_at',
            field=models.DateTimeField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='last_test_at',
            field=models.DateTimeField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='published_at',
            field=models.DateTimeField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='readme_updated_at',
            field=models.DateTimeField(blank=True, db_index=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='status',
            field=models.CharField(choices=[('NOT_STARTED', 'Not Started'), ('PLANNING', 'Planning'),
                                            ('WRITING', 'Writing'), ('DRAFT', 'Draft'),
                                            ('OPTIMIZED', 'Optimized'), ('PUBLISHED', 'Published')],
                                   db_index=True,
                                   default='NOT_STARTED',
                                   help_text='Related to the publishing of the asset',
                                   max_length=20),
        ),
        migrations.AlterField(
            model_name='asset',
            name='sync_status',
            field=models.CharField(blank=True,
                                   choices=[('PENDING', 'Pending'), ('ERROR', 'Error'), ('OK', 'Ok'),
                                            ('WARNING', 'Warning'), ('NEEDS_RESYNC', 'Needs Resync')],
                                   db_index=True,
                                   default=None,
                                   help_text='Internal state automatically set by the system based on sync',
                                   max_length=20,
                                   null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='test_status',
            field=models.CharField(blank=True,
                                   choices=[('PENDING', 'Pending'), ('ERROR', 'Error'), ('OK', 'Ok'),
                                            ('WARNING', 'Warning'), ('NEEDS_RESYNC', 'Needs Resync')],
                                   db_index=True,
                                   default=None,
                                   help_text='Internal state automatically set by the system based on test',
                                   max_length=20,
                                   null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='title',
            field=models.CharField(blank=True, db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='asset',
            name='visibility',
            field=models.CharField(
                choices=[('PUBLIC', 'Public'), ('UNLISTED', 'Unlisted'), ('PRIVATE', 'Private')],
                db_index=True,
                default='PUBLIC',
                help_text="It won't be shown on the website unleast the status is published",
                max_length=20),
        ),
        migrations.AlterField(
            model_name='asset',
            name='with_solutions',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='asset',
            name='with_video',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
