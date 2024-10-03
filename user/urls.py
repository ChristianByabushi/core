from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("login/", views.login, name="login"), 
    path("logout/", views.logout_view, name="logout"), 
    path('locataires/', views.locataires, name='locataires'),
    path('locataires/supprimer/<int:id>/', views.supprimerlocataire, name='supprimerlocataire'),
    path('locataires/creer/', views.creerlocataire, name='creerlocataire'),
    path('locataires/editer/<int:id>/', views.editerlocataire, name='editerlocataire'),
    
    
    path("mon-compte/", views.compte, name="moncompte"), 
    path("mon-compte/edit/", views.editerMoncompte, name="editerMoncompte"),
    path("mon-compte/changer-mot-passe/", views.changeMotdepasse, name="changeMotdepasse"),
    path("comptes/ajouter-utilisateur/", views.ajouterUtilisateur, name="ajouterUtilisateur"),
    path("comptes/<int:userId>/supprimer-utilisateur/", views.supprimerUtilisateur, name="supprimerUtilisateur"), 
    path("comptes/<int:userId>/reinitialiser-mot-de-passe-utilisateur/", views.reinitialiserMotDepasseUtilisateur, name="reinitialiserMotDepasseUtilisateur"), 
    path("comptes/<int:userId>/modifier-utilisateur/", views.modifierrUtilisateur, name="modifierrUtilisateur"),
    path("comptes/<int:userId>/get-utilisateur/", views.getUtilisateur, name="getUtilisateur"),
    # path("", views.messaging, name="contact-us"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
