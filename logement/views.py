from django.shortcuts import render, redirect ,get_object_or_404
from contrat.models import Locataire, Contrat, Dette, Paiement
from logement.models import Logement
from user.models import User, Locataire
from django.contrib import messages
from .forms import LogementForm 

def index_dashboard(request):
    return render(request, 'dashboard/index.html',
           {
               'contracts_last_week':Contrat.contracts_last_week(),
               'contracts_last_month':Contrat.contracts_last_month(),
               'contracts_last_year':Contrat.contracts_last_year(),
               'payments_last_week':Paiement.payments_last_week(),
               'payments_last_month':Paiement.payments_last_month(),
               'total_contracts':Paiement.total_contracts(),
               'total_logements':Logement.total_logements(), 
               'total_locataires':Locataire.total_locataires(),
               'total_paiements':Paiement.total_paiements(), 
               'contrats': Contrat.objects.all()[:5]
           }) 

def logement(request):
    logements = Logement.objects.all()
    return render(request,'logement/main.html',{
        'logements':logements
    })


def creer_logement(request):
    if request.method == "POST":
        form = LogementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Creation informations sur le logement réussie avec succès!")
            return redirect("logements")
        else:
            errors = form.errors.as_text()
            messages.error(request, f"La création des informations sur le logement a échoué. {errors}")
    else:
        form = LogementForm()
    return render(request, "logement/forms/ajouter.html", {"form": form})


def supprimer_logement(request,id):
    logement = get_object_or_404( Logement, id=id)
    logement.delete()
    messages.success(request, "Le logement a été supprimé avec succès.")
    return redirect("logements")


def editer_logement(request,id):
    logement = get_object_or_404(Logement, id=id)
    if request.method == "POST":
        form = LogementForm(request.POST, instance=logement)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, "Les informations sur ce logement ont été editées avec succès!")
            return redirect("logements")
        else:
            errors = form.errors.as_text()
            messages.error(request, f"La modification de infos sur ce logement ont échoué. {errors}")
    else:
        form = LogementForm(instance=logement)
    return render(request, "logement/forms/editer.html", {"logement": logement, 'form':form}) 