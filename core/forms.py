from django import forms
from .models import Election, Option, Voter

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['theme', 'description', 'start_date', 'end_date', 'type', 'document']
        widgets = {
            'theme': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Eleição para Reitor 2025'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva os objetivos e regras da eleição...'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'document': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
        help_texts = {
            'theme': 'Título principal da eleição',
            'description': 'Informações detalhadas sobre a eleição',
            'start_date': 'Data e hora de início da votação',
            'end_date': 'Data e hora de encerramento da votação',
            'type': 'Escolha se permite voto único ou múltiplo',
            'document': 'Documento oficial da eleição (edital, regulamento, etc.)'
        }


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Chapa 1 - João Silva e Maria Santos'
            })
        }
        labels = {
            'name': 'Nome do Candidato/Opção'
        }


class VoterForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do eleitor'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@uems.br ou email@gmail.com'
            })
        }
        labels = {
            'name': 'Nome Completo',
            'email': 'E-mail'
        }
        help_texts = {
            'email': 'Use o e-mail institucional (@uems.br) ou Gmail do eleitor'
        }