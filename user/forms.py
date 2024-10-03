from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import User, Locataire
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
    
class LocataireForm(forms.ModelForm):
    class Meta:
        model = Locataire
        fields = '__all__'
        
class LocataireFormEditer(forms.ModelForm):
    class Meta:
        model = Locataire
        fields = ['adresse', 'first_name', 'last_name','numeroTel',
                  'email', 'password']