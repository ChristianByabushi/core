from django.shortcuts import render,get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
import json
from django.http import JsonResponse ,HttpResponse
from django.shortcuts import redirect 
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password, check_password 
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required,login_not_required
from user.models import User
from django.contrib import messages
from user.models import Locataire  


def creer_un_compte(request):
    if request.user.role=='admin':
        print('test')
    return render(request, 'comptes/register.html') 

def locataires(request):
    locataires = Locataire.objects.all()
    return render(request,'locataires/main.html',{
        'locataires':locataires
    })

# LocataireForm
from .forms import LocataireForm,LocataireFormEditer
def creerlocataire(request):
    if request.method == "POST":
        form = LocataireForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Creation locataire réussie avec succès!")
            return redirect("locataires")
        else:
            errors = form.errors.as_text()
            messages.error(request, f"Echec dans la creation du locataire, à cause de : {errors}")
    else:
        form = LocataireForm()
    return render(request, "locataires/forms/ajouter.html", {"form": form})


def supprimerlocataire(request,id):
    logement = get_object_or_404( Locataire, id=id)
    logement.delete()
    messages.success(request, "Le locataire a été supprimé avec succès.")
    return redirect("locataires")


def editerlocataire(request, id):
    locataire = get_object_or_404(Locataire, id=id) 
    if request.method == "POST" :
        adresse = request.POST.get('adresse')
        first_name = request.POST.get('first_name')  
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        numeroTel = request.POST.get('numeroTel')
        locataire.last_name=last_name or locataire.last_name
        locataire.numeroTel=numeroTel or locataire.numeroTel 
        locataire.first_name=first_name or locataire.first_name
        locataire.adresse=adresse or locataire.adresse
        locataire.email=email  or locataire.email
        form = LocataireFormEditer(instance=locataire)
        if form.is_valid():
            locataire.save() 
            messages.error(request, f"La modification du profile du locataire reussi avec succès") 
            return redirect('locataires')
        else:
            errors = form.errors.as_text()
            messages.error(request, f"La modification de infos sur ce logement ont échoué. {errors}") 
    else:
        form = LocataireForm(instance=locataire)
    return render(request, "locataires/forms/editer.html", {"locataire": locataire}) 


@login_not_required  
def register(request):
    if request.method != 'POST':
        return render(request, "comptes/register.html")
    
    # Get data from the POST request
    email = request.POST.get("email")
    password1 = request.POST.get("password1")
    firstname = request.POST.get("firstname")
    password2 = request.POST.get("password2")

    # Validate form inputs
    if password1 != password2:
        messages.error(request, "Les mots de passe ne correspondent pas.")
        return render(request, "comptes/register.html", {
            'email': email,
            'firstname': firstname
        })

    if User.objects.filter(email=email).exists():
        messages.error(request, "Un utilisateur avec cet e-mail existe déjà.")
        return render(request, "comptes/register.html", {
            'email': email,
            'firstname': firstname
        })

    # Create the user
    user = Locataire.objects.create(
        email=email,
        password=make_password(password1),  # Hash the password here
        role="guest",
        first_name=firstname
    )
    user.save()

    # Send success message and redirect to login
    messages.success(request, 'Utilisateur créé avec succès, veuillez vous connecter.')
    return redirect('login')


@login_not_required
def login(request):
    if request.user.is_authenticated: 
        return render(request, 'configuration/connected.html')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user) 
            return redirect('index')
        else:
            error_message = 'Utilisateur ou mot de passe incorrect' 
            return render(request, 'comptes/login.html', {'error_message': error_message})
    return render(request, "comptes/login.html") 

def compte(request):
    context={}
    # if User.objects.filter(id=request.user.id, groups__name='titulaire').exists():
        #  context['listesClasses'] = Classe.objects.filter(titulaire_id=request.user.id).all()
    # context['institution'] = Institution.objects.last()
    return render(request, 'comptes/moncompte.html', context)
def reinitialiserMotDepasseUtilisateur(request, userId):
    if request.method == 'POST':
        try:
            user = User.objects.get(pk=userId)
            new_password = "changemoi"  
            user.set_password(new_password)
            user.save()
            return JsonResponse({'success': True, 'message': 'Mot de passe réinitialisé avec succès !', 'new_password': new_password})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur introuvable.'})
    else:
        return JsonResponse({'error': 'Requête invalide.'})


def logout_view(request):
    logout(request) 
    return  redirect('index')

def changeMotdepasse(request):
    ancien_pwd = request.POST.get('ancienPwd')
    nouveau_pwd = request.POST.get('nouveauPwd')
    confirm_nouveau_pwd = request.POST.get('confirmnouveauPwd')
    if not all([nouveau_pwd,ancien_pwd, confirm_nouveau_pwd,]):
            return JsonResponse({'success': False, 'message': "Veuillez compléter tous les champs s'il vous plaît."}, status=400)

    if nouveau_pwd != confirm_nouveau_pwd:
        return JsonResponse({'success': False, 'message': 'Les mots de passe ne correspondent pas.'})

    user = request.user
    if not check_password(ancien_pwd, user.password):
        return JsonResponse({'success': False, 'message': 'Ancien mot de passe incorrect.'}, status=200)

    user.password = make_password(nouveau_pwd)
    user.save()
    # messages.success(request, 'Mot de passe modifié avec succès.')
    return JsonResponse({'success': True, 'message': 'Mot de passe modifié avec succès.'})

def editerMoncompte(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')  
        last_name = request.POST.get('last_name')  
        email = request.POST.get('email')  
        pwd = request.POST.get('pwd') 
        avatar =  request.FILES.get('avatar') 

        if not all([login, first_name, last_name, pwd]):
            return JsonResponse({'success': False, 'message': "Veuillez compléter tous les champs s'il vous plaît."}, status=400)
        emailcheck = User.objects.filter(email=email).exclude(email=email)
        if emailcheck.exists():
            return JsonResponse({'success': False, 'message': "Lemail choisi existe deja, veuillez changer svp!"}, status=400)
            
        if not check_password(pwd, request.user.password):
            return JsonResponse({'success': False, 'message': 'Mot de passe incorrect.'}, status=200)

        userAediter = User.objects.get(pk=request.user.id) 
        userAediter.email = email 
        userAediter.first_name = first_name 
        userAediter.last_name = last_name 
        if avatar:
            userAediter.avatar =avatar
        userAediter.save()
        return JsonResponse({'success': True,  'message': 'Modifications du compte effectuée avec succes!'}) 
   

def ajouterUtilisateur(request):
    login = request.POST.get('login')
    noms = request.POST.get('noms')
    role = request.POST.get('role')
    password = request.POST.get('password')
    groups = request.POST.getlist('groups[]')  

    # Create the user
    user = User.objects.create_user(login=login, noms=noms, password=password)  # Replace with your password generation logic
    
    # Set user attributes
    user.role = role
    user.save()


    # Assign user to groups
    for group_id in groups:
        group = Group.objects.get(pk=group_id)
        user.groups.add(group)

    # Redirect or return a success message
    return JsonResponse({'success': True, 'message': 'Utilisateur créé avec succès'})



def modifierrUtilisateur(request, userId):
    try:
        user = User.objects.get(pk=userId)
        groups_string = request.POST.get('login')
        noms = request.POST.get('noms')
        role = request.POST.get('role') 

        user.noms = noms
        user.role = role

        # delete first all user groups
        user.groups.clear()

        # Convert the stringified groups data into a list of group IDs
        groups_string = request.POST.get('groups')
        new_groups = json.loads(groups_string)

        # Add new groups
        for group_id in new_groups:
            group = Group.objects.get(pk=group_id)
            user.groups.add(group)
        user.save()
        return JsonResponse({'success': True, 'message': 'User groups updated successfully'})
        
    except Group.DoesNotExist or User.DoesNotExist :
            return JsonResponse({'success': False, 'message': "Classe non trouvée."}, status=404) 
    

def getUtilisateur(request, userId):
    try:
        userResult = User.objects.get(pk=userId) 
        userGroups=[] 
        for groupe in userResult.groups.all():
            userGroups.append({
                'id':groupe.id,
                'name':groupe.name
            }) 
        output={
            'groups': userGroups, 
            'login':userResult.login,
            'noms':userResult.noms,
            'role': userResult.role,
        }
        
        return JsonResponse({'success': True,  'utilisateur':  output}) 
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': "Utilisateur non trouvée."}, status=404)

def supprimerUtilisateur(request, userId):
    try:
        userAsupprimer = User.objects.get(pk=userId) 
        userAsupprimer.delete() 
        return JsonResponse({'success': True,  'message': 'Utilisateur supprimé avec succès!'}) 
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': "Utilisateur non trouvé."}, status=404)


