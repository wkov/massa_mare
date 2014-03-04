__author__ = 'sergi'
# from django.forms import forms, ModelForm
from django import forms
from .models import Comanda, Incomanda, Fornada, Despesa, Farina, UserProfile, Client, Status

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user",)

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client

class ComandaForm(forms.ModelForm):
    class Meta:
        model = Comanda
        exclude = ('fornada',)

class IncomandaForm(forms.ModelForm):
    class Meta:
        model = Incomanda

class FornadaForm(forms.ModelForm):
    class Meta:
        model = Fornada

class FarinaForm(forms.ModelForm):
    class Meta:
        model = Farina
        exclude = ("preu", "nom")

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
