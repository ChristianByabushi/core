from django import forms
from .models import Contrat, Paiement
from django.core.exceptions import ValidationError
class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = '__all__'
        widgets = {
            'datedebut': forms.DateInput(attrs={'type': 'date', 'class':'form-control form-control'}),
            'datefin': forms.DateInput(attrs={'type': 'date', 'class':'form-control form-control'}),
            'montantgaranti': forms.NumberInput(attrs={'type': 'number', 'placeholder': 'Entrer le garanti en dollars'}),
            'termes_du_contrat': forms.Textarea(attrs={'required': True}), 
        }
class ContratForm(forms.ModelForm):
    class Meta:
        model = Contrat
        fields = ['termes_du_contrat', 'logement', 'locataire', 'datedebut', 'datefin', 'montantgaranti']
        widgets = {
            'datedebut': forms.DateInput(attrs={'type': 'date', 'class':'form-control form-control'}),
            'datefin': forms.DateInput(attrs={'type': 'date', 'class':'form-control form-control'}),
            'montantgaranti': forms.NumberInput(attrs={'type': 'number', 'placeholder': 'Entrer le garanti en dollars'}),
            'termes_du_contrat': forms.Textarea(attrs={'required': True}), 
        }
    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get("datedebut")
        date_fin = cleaned_data.get("datefin")
        logement = cleaned_data.get("logement")

        if date_debut and date_fin and date_debut > date_fin:
            raise ValidationError("La date du début ne peut pas être supérieure à la date de fin.")
        
        if logement and date_debut and date_fin:
            contrats = Contrat.objects.filter(logement=logement).exclude(pk=self.instance.pk)

            for contrat in contrats:
                if (date_debut < contrat.datefin and date_fin > contrat.datedebut):
                    raise ValidationError(
                        'Les dates du contrat se chevauchent avec un contrat existant pour ce logement.',
                        code='date_overlap'
                    )

        return cleaned_data
    