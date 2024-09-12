from django import forms
from .models import Profile, Submission, ThematicAxis, Modality
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nome','cpf', 'whatsapp', 'comprovante_pagamento'] #alteração
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}), #alteração
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp'}),
            'comprovante_pagamento': forms.FileInput(attrs={'class': 'form-control'}),
        }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['thematic_axis', 'modality', 'arquivo']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Certifique-se de que o email é obrigatório

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

