from django.db import models
from user.models import Locataire  
from datetime import datetime
from logement.models import Logement
from django.db.models import Sum 
from user.models import Locataire 
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
class Contrat(models.Model):
    termes_du_contrat = models.TextField() 
    logement = models.ForeignKey(Logement, on_delete=models.PROTECT) 
    locataire = models.ForeignKey(Locataire,on_delete=models.PROTECT)
    datedebut= models.DateField()
    datefin = models.DateField() 
    montantgaranti = models.DecimalField(max_digits=16,decimal_places=3)
    class Meta:
        ordering=['-id'] 
    
    def __str__(self):
        return f"Contrat#{self.id}"
    
    def total_payments(self):
        return self.paiement_set.aggregate(total=Sum('montant'))['total'] or 0

    def debt(self):
        return self.montantgaranti - self.total_payments()
    
    def update_debts(self):
        total_debt = self.debt()
        if total_debt > 0:
            Dette.objects.update_or_create(
                contrat=self,
                defaults={'montant': total_debt, 'date_echeance': self.datefin, 'statut': 'encours'}
            )
        else:
            Dette.objects.filter(contrat=self).update(statut='regle') 
    def clean(self):
        """
        Custom validation to check for overlapping contracts
        """
        contrats = Contrat.objects.filter(logement=self.logement).exclude(pk=self.pk)

        for contrat in contrats:
            if (self.datedebut < contrat.datefin and self.datefin > contrat.datedebut):
                raise ValidationError(
                    ('Les dates du contrat se chevauchent avec un contrat existant pour ce logement.'),
                    code='date_overlap'
                )

    @classmethod
    def contracts_last_week(cls):
        one_week_ago = datetime.now() - timedelta(days=7)
        return cls.objects.filter(datedebut__gte=one_week_ago)

    @classmethod
    def contracts_last_month(cls):
        one_month_ago = datetime.now() - timedelta(days=30)
        return cls.objects.filter(datedebut__gte=one_month_ago)

    @classmethod
    def contracts_last_year(cls):
        one_year_ago = datetime.now() - timedelta(days=365)
        return cls.objects.filter(datedebut__gte=one_year_ago)

class Paiement(models.Model):
    contrat = models.ForeignKey(Contrat, on_delete=models.PROTECT)
    date_paiement = models.DateField()
    montant= models.DecimalField(max_digits=16,decimal_places=3) 
    statut = models.CharField(max_length=50, choices=[('paye', 'payé'), ('retard', 'retard'),('avance', 'avance')]) 
    class Meta:
        ordering=['-date_paiement'] 
    @classmethod
    def payments_last_week(cls):
        one_week_ago = datetime.now() - timedelta(days=7)
        return cls.objects.filter(date_paiement__gte=one_week_ago)

    @classmethod
    def payments_last_month(cls):
        one_month_ago = datetime.now() - timedelta(days=30)
        return cls.objects.filter(date_paiement__gte=one_month_ago)
    
    @classmethod
    def total_contracts(cls):
        return cls.objects.count()
    
    @classmethod
    def total_paiements(cls):
        return Paiement.objects.aggregate(total=Sum('montant'))['total'] or 0

    @classmethod
    def payments_last_year(cls):
        one_year_ago = datetime.now() - timedelta(days=365)
        return cls.objects.filter(date_paiement__gte=one_year_ago)

class Dette(models.Model):
    contrat = models.ForeignKey(Contrat, on_delete=models.PROTECT)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_echeance = models.DateField()
    statut = models.CharField(max_length=50, choices=[('regle', 'reglé'), ('encours', 'en cours')])

    def __str__(self):
        return f"Dette#{self.id} for Contrat#{self.contrat.id}"