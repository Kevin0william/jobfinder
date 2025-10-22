# forms.py
from django import forms
from .models import AvisSite

class AvisSiteForm(forms.ModelForm):
    class Meta:
        model = AvisSite
        fields = ['note', 'commentaire']
        widgets = {
            'note': forms.NumberInput(attrs={
                'min': 1, 'max': 5,
                'class': 'form-control',
                'placeholder': 'Note (1 à 5)'
            }),
            'commentaire': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Écris ton avis ici...',
                'class': 'form-control'
            })
        }
