from django import forms 
from logement.models import Logement 

class LogementForm(forms.ModelForm):
    class Meta:
        model = Logement
        fields = '__all__'