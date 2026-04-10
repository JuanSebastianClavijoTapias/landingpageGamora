from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'company', 'email', 'phone', 'need']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'field__input', 'placeholder': 'Tu nombre'}
            ),
            'company': forms.TextInput(
                attrs={'class': 'field__input', 'placeholder': 'Nombre de tu empresa'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'field__input', 'placeholder': 'correo@empresa.com'}
            ),
            'phone': forms.TextInput(
                attrs={'class': 'field__input', 'placeholder': 'Telefono o WhatsApp'}
            ),
            'need': forms.Textarea(
                attrs={
                    'class': 'field__input field__input--textarea',
                    'placeholder': 'Cuentanos que proceso quieres digitalizar o acelerar.',
                    'rows': 5,
                }
            ),
        }
        labels = {
            'need': 'Necesidad',
        }