"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from django.urls import path
from logement.views import *
from contrat.views import * 
from user.views import * 



from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('comptes/', include('user.urls')),

    # logement
    path('',index_dashboard, name='index'),
    path('logements/',logement, name='logements'),
    path('logements/creer/',creer_logement, name='creer_logement'),
    path('logements/supprimer/<int:id>/',supprimer_logement, name='supprimer_logement'),
    path('logements/editer/<int:id>/',editer_logement, name='editer_logement'),

    # contrat
    path('contrats/',contrats, name='contrats'),
    path('contrats/supprimer/<int:id>/',supprimer_contrat, name='supprimer_contrat'),
    path('contrats/editer/<int:id>/',editer_contrat, name='editer_contrat'),
    path('contrats/creer/',creer_contrat, name='creer_contrat'),
    path('contrats/imprimer/<int:id>/',generate_pdf_contrat, name='generate_pdf_contrat'),

    
    #paiements
    path('paiements/',paiements, name='paiements'),
    path('paiements/supprimer/<int:id>/',supprimer_paiements, name='supprimer_paiement'),
    path('paiements/editer/<int:id>/',editer_paiements, name='editer_paiement'),
    path('paiements/creer/',creer_paiements, name='creer_paiement'),
    path('payements/',creer_paiements, name='locatairespayements'),
    path('payements/imprimer/<int:id>/',generate_pdf_paiment, name='generate_pdf_paiment'),
    
    #dettes
    path('dettes/',dettes, name='dettes'),
    path('dettes/supprimer/<int:id>/',supprimer_dettes, name='supprimer_dettes'),
    path('dettes/editer/<int:id>/',editer_dettes, name='editer_dettes'),
    path('dettes/creer/',creer_dettes, name='creer_dettes'),
    
                    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()