# Generated by Django 5.1.1 on 2024-09-16 23:20

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_submission_arquivo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='arquivo',
            field=models.FileField(upload_to='submissoes/', validators=[core.models.validate_file_extension], verbose_name='Arquivo Submetido'),
        ),
    ]