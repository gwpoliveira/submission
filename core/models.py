from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class ThematicAxis(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Modality(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(verbose_name='Nome completo:', max_length=255, default='')
    cpf = models.CharField(verbose_name='CPF:', max_length=14, unique=True, blank=True, null=True)
    whatsapp = models.CharField(verbose_name='Whatsapp:', max_length=15)
    comprovante_pagamento = models.FileField(verbose_name='Comprovante de inscrição no congresso:', upload_to='comprovantes/', blank=False, null=False)

def validate_file_extension(value):
    if not value.name.endswith('.doc') and not value.name.endswith('.docx'):
        raise ValidationError("Apenas arquivos .doc ou .docx são permitidos.")

class Component(models.Model):
    submission = models.ForeignKey('Submission', related_name='components', on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14)
    email = models.EmailField()

    def __str__(self):
        return self.nome

class Submission(models.Model):
    STATUS_CHOICES = [
        ('EM_ANALISE', 'Em Análise'),
        ('DEFERIDO', 'Deferido'),
        ('INDEFERIDO', 'Indeferido'),
    ]
    title = models.CharField(max_length=255, verbose_name='Título do Trabalho')  # Novo campo
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    thematic_axis = models.ForeignKey(ThematicAxis, verbose_name='Eixo Temático', on_delete=models.CASCADE)
    modality = models.ForeignKey(Modality, verbose_name='Modalidade', on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to='submissoes/', verbose_name='Arquivo Submetido', validators=[validate_file_extension])
    comprovante = models.FileField(upload_to='comprovantes/', null=True, blank=True, verbose_name='Comprovante de Pagamento')
    data_envio = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EM_ANALISE')
    observacao = models.TextField(verbose_name='Observação', blank=True, default='')
    acceptance_letter_generated = models.BooleanField(default=False)  # Novo campo

    def __str__(self):
        return f'{self.title} - {self.user.user.username} - {self.thematic_axis.name}'




