from django import forms
from .models import Profile, Submission, Component
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import modelformset_factory

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nome', 'cpf', 'whatsapp', 'comprovante_pagamento']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp'}),
            'comprovante_pagamento': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['whatsapp'].required = True  # Certifique-se de que está definido como obrigatório

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['title', 'thematic_axis', 'modality', 'arquivo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Trabalho'}),
            'thematic_axis': forms.Select(attrs={'class': 'form-select'}),  # Campo de seleção
            'modality': forms.Select(attrs={'class': 'form-select'}),       # Campo de seleção
            'arquivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['nome', 'cpf', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))  # Certifique-se de que o email é obrigatório

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

# Formset para múltiplos componentes
ComponentFormSet = modelformset_factory(Component, form=ComponentForm, extra=1)
