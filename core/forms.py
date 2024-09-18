from django import forms
from .models import Profile, Submission, Component
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django import forms
from django.forms import modelformset_factory

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
        fields = ['title', 'thematic_axis', 'modality', 'arquivo']

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['nome', 'cpf', 'email']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Certifique-se de que o email é obrigatório

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Formset para múltiplos componentes
ComponentFormSet = modelformset_factory(Component, form=ComponentForm, extra=1)