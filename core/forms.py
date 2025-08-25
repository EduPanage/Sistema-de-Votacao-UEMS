from django import forms
from .models import Election
from .models import Option
from .models import Voter

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['title', 'description', 'start_date', 'end_date', 'type', 'is_published']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['name']
        

class VoterForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ['name', 'email']

        
