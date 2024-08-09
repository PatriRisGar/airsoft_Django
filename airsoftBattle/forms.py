from django import forms
from django.contrib.auth.forms import UserCreationForm
from airsoftBattle.models import Partida,Usuario


class PartidaForm(forms.ModelForm):
    class Meta:
        model = Partida
        fields = ['fechaInicio', 'horaInicio', 'fechaFin', 'horaFin']
        widgets = {
            'fechaInicio': forms.DateInput(attrs={'type': 'date'}),
            'horaInicio': forms.TimeInput(attrs={'type': 'time'}),
            'fechaFin': forms.DateInput(attrs={'type': 'date'}),
            'horaFin': forms.TimeInput(attrs={'type': 'time'}),
        }




class RegistroUsuarioForm(UserCreationForm):
  class Meta:
    model= Usuario
    fields = ['username', 'email', 'password1', 'password2']