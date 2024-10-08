# Generated by Django 5.1.1 on 2024-09-11 20:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Modality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ThematicAxis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='Nome Desconhecido', max_length=255, verbose_name='Nome completo:')),
                ('cpf', models.CharField(blank=True, max_length=14, null=True, unique=True, verbose_name='CPF:')),
                ('whatsapp', models.CharField(max_length=15, verbose_name='Whatsapp:')),
                ('comprovante_pagamento', models.FileField(upload_to='comprovantes/', verbose_name='Comprovante de inscrição no congresso:')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo', models.FileField(upload_to='submissoes/')),
                ('data_envio', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('EM_ANALISE', 'Em Análise'), ('DEFERIDO', 'Deferido'), ('INDEFERIDO', 'Indeferido')], default='EM_ANALISE', max_length=20)),
                ('observacao', models.TextField(blank=True, null=True, verbose_name='Observação:')),
                ('modality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.modality', verbose_name='Modalidade:')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.profile')),
                ('thematic_axis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.thematicaxis', verbose_name='Eixo Tematico:')),
            ],
        ),
    ]
