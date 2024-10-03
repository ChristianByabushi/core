from django.shortcuts import render, redirect, get_object_or_404
from contrat.models import Contrat
from user.models import Locataire
from logement.models import Logement
from django.contrib import messages
from .forms import ContratForm, PaiementForm


from django.shortcuts import render
from .models import Contrat, Logement, Locataire, Paiement
from django.db.models import Q


def contrats(request):
    contrats = Contrat.objects.all()

    # Get search parameters from the GET request
    locataire_name = request.GET.get("locataire") or ""
    logement_id = request.GET.get("logement")
    debut_date = request.GET.get("debutDate")
    fin_date = request.GET.get("dateFin")

    # Filter contrats based on search inputs
    if locataire_name:
        contrats = contrats.filter(
            Q(locataire__first_name__icontains=locataire_name)
            | Q(locataire__last_name__icontains=locataire_name)
        )
    if logement_id:
        contrats = contrats.filter(logement_id=logement_id)
    if debut_date:
        contrats = contrats.filter(datedebut__gte=debut_date)
    if fin_date:
        contrats = contrats.filter(datefin__lte=fin_date)

    # Fetch logements and locataires for the dropdown options
    logements = Logement.objects.all()
    locataires = Locataire.objects.all()

    context = {
        "contrats": contrats,
        "logements": logements,
        "locataires": locataires,
        "filters": {
            "locataire": locataire_name,
            "logement": logement_id,
            "debutDate": debut_date,
            "dateFin": fin_date,
        },
    }

    return render(request, "contrat/index.html", context)


from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib import messages


def creer_contrat(request):
    logements = Logement.objects.all()
    locataires = Locataire.objects.all()
    if request.method == "POST":
        form = ContratForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Creation du contrat réussi avec succès!")
            return redirect("contrats")
        else:
            errors = form.errors.as_text()
            messages.error(request, f"La création du contrat a échoué. {errors}")
    else:
        form = ContratForm()

    return render(
        request,
        "contrat/ajouter.html",
        {"logements": logements, "locataires": locataires},
    )


def supprimer_contrat(request, id):
    contrat = get_object_or_404(Contrat, id=id)
    contrat.delete()
    messages.success(request, "Le contrat a été supprimé avec succès.")
    return redirect("contrats")


def editer_contrat(request, id):
    contrat = get_object_or_404(Contrat, id=id)
    logements = Logement.objects.all()
    locataires = Locataire.objects.all()
    if request.method == "POST":
        form = ContratForm(request.POST, instance=contrat)
        if form.is_valid():
            form.save()
            messages.success(request, "Le contrat a été modifié avec succès!")
            return redirect("contrats")
        else:
            errors = form.errors.as_text()
            messages.error(request, f"La modification du contrat a échoué : {errors}")
    else:
        form = ContratForm(instance=contrat)
    return render(
        request,
        "contrat/editer.html",
        {
            "contrat": contrat,
            "logements": logements,
            "locataires": locataires,
            "form": form,
        },
    )


from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib.enums import TA_CENTER
import os
from datetime import datetime
from django.http import HttpResponse
from django.conf import settings


def generate_pdf_contrat(request, id):
    contrat = Contrat.objects.filter(pk=id).first()
    if contrat:
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="Contrat-{contrat.id}#{contrat.locataire.email}.pdf"'
        )

        pdf = SimpleDocTemplate(
            response,
            pagesize=A4,
        )

        logo_path = os.path.join(settings.BASE_DIR, "static/assets/img/logo.jpg")

        elements = []

        if os.path.exists(logo_path):
            logo = Image(logo_path, 2 * inch, 1 * inch)
            elements.append(logo)

        styles = getSampleStyleSheet()
        title_style = styles["Heading1"]
        title_style.alignment = TA_CENTER

        elements.append(Paragraph("LOYER", title_style))
        elements.append(
            Paragraph(
                f"CONTRAT LOCATION {contrat.logement.type}#{contrat.id}", title_style
            )
        )
        elements.append(Spacer(1, 14))

        elements.append(
            Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles["Normal"])
        )
        elements.append(
            Paragraph(
                f"Partenaire: {contrat.locataire.first_name}, {contrat.locataire.last_name}",
                styles["Normal"],
            )
        )
        elements.append(
            Paragraph(f"Email: {contrat.locataire.email}", styles["Normal"])
        )
        elements.append(Spacer(1, 14))

        elements.append(Paragraph(f"{contrat.termes_du_contrat}", styles["Normal"]))
        elements.append(Spacer(1, 14))
        elements.append(
            Paragraph(
                f"Montant total (Garanti): {contrat.montantgaranti} $", styles["Normal"]
            )
        )
        elements.append(Spacer(1, 14))

        elements.append(Paragraph(f"Date debut: {contrat.datedebut}", styles["Normal"]))
        elements.append(Paragraph(f"Date FIn: {contrat.datefin}", styles["Normal"]))

        pdf.build(elements)

        return response
    else:
        return HttpResponse("Desole le contrat de commande est introuvable")



def generate_pdf_paiment(request, id):
    paiement = Paiement.objects.filter(pk=id).first()
    if paiement:
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="Paiement-{paiement.contrat.id}#{paiement.contrat.locataire.email}.pdf"'
        )

        pdf = SimpleDocTemplate(
            response,
            pagesize=A4,
        )

        logo_path = os.path.join(settings.BASE_DIR, "static/assets/img/logo.jpg")

        elements = []

        if os.path.exists(logo_path):
            logo = Image(logo_path, 2 * inch, 1 * inch)
            elements.append(logo)

        styles = getSampleStyleSheet()
        title_style = styles["Heading1"]
        title_style.alignment = TA_CENTER

        elements.append(Paragraph("LOYER", title_style))
        elements.append(
            Paragraph(
                f"PAIEMENT {paiement.contrat.logement.type}#{paiement.contrat.id}", title_style
            )
        )
        elements.append(Spacer(1, 14))

        elements.append(
            Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles["Normal"])
        )
        elements.append(
            Paragraph(
                f"Partenaire: {paiement.contrat.locataire.first_name}, {paiement.contrat.locataire.last_name}",
                styles["Normal"],
            )
        )
        elements.append(
            Paragraph(f"Email: {paiement.contrat.locataire.email}", styles["Normal"])
        )
        elements.append(Spacer(1, 14))

        elements.append(Paragraph(f"Montant payé :{paiement.montant}", styles["Normal"]))
        elements.append(Paragraph(f" Tous les payements :{paiement.contrat.total_payments()}", styles["Normal"]))
        elements.append(Paragraph(f" Montant garanti :{paiement.contrat.montantgaranti}", styles["Normal"]))
        elements.append(Paragraph(f" Dettes :{paiement.contrat.debt()}", styles["Normal"]))
        elements.append(Spacer(1, 14))

        elements.append(Spacer(1, 14))

        elements.append(Paragraph(f"Contrat/date debut: {paiement.contrat.datedebut}", styles["Normal"]))
        elements.append(Paragraph(f"Date FIn: {paiement.contrat.datefin}", styles["Normal"]))

        pdf.build(elements)

        return response
    else:
        return HttpResponse("Desole le contrat de commande est introuvable")


# paiements 
def paiements(request):
    logements = Logement.objects.all()
    locataires = Locataire.objects.all()
    paiements = Paiement.objects.all()

    locataire_name = request.GET.get("locataire") or ""
    logement_id = request.GET.get("logement")
    debut_date = request.GET.get("debutDate")
    fin_date = request.GET.get("dateFin")

    # Filter contrats based on search inputs
    if locataire_name:
        paiements = paiements.filter(
            Q(contrat__locataire__first_name__icontains=locataire_name)
            | Q(contrat__locataire__last_name__icontains=locataire_name)
        )
    if logement_id:
        paiements = paiements.filter(contrat__logement_id=logement_id)
    if debut_date:
        paiements = paiements.filter(date_paiement__gte=debut_date)
    if fin_date:
        paiements = paiements.filter(date_paiement__lte=fin_date)

    return render(
        request,
        "paiement/index.html",
        {
            "logements": logements,
            "locataires": locataires,
            "paiements": paiements,
            "filters": {
                "locataire": locataire_name,
                "logement": logement_id,
                "debutDate": debut_date,
                "dateFin": fin_date,
            },
        },
    )


def creer_paiements(request):
    logements = Logement.objects.all()
    locataires = Locataire.objects.all()
    contrats = Contrat.objects.all()

    if request.method == "POST":
        form = PaiementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Paiement réussi!")
            return redirect("paiements")
        else:
            errors = form.errors.as_text()
            messages.error(request, f"Le paiement  a échoué pour des raisons :{errors}")
    else:
        form = PaiementForm()

    return render(
        request,
        "paiement/ajouter.html",
        {"logements": logements, "locataires": locataires, "contrats": contrats},
    )


def supprimer_paiements(request,id):
    paiement = get_object_or_404( Paiement, id=id)
    paiement.delete()
    messages.success(request, "Enregistrement payement supprimé avec succès.")
    return redirect("paiements")

def editer_paiements(request,id):
    logements = Logement.objects.all()
    locataires = Locataire.objects.all()
    contrats = Contrat.objects.all()
    paiement = get_object_or_404(Paiement, id=id)
    if request.method == "POST":
        form = PaiementForm(request.POST, instance=paiement)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, "Paiement edite avec succès!")
            return redirect("paiements")
        else:
            errors = form.errors.as_text()
            messages.error(request, f"Edition infos paiements échoué : {errors}")
    else:
        form = PaiementForm(instance=paiement)
    return render(request, "paiement/editer.html",
                   {'paiement':paiement,"logements": logements, "locataires": locataires, "contrats": contrats},
                  ) 


# dette
def dettes(request):
    return render("")


def creer_dettes(request):
    return render("")


def supprimer_dettes(request):
    return render("")


def editer_dettes(request):
    return render("")
