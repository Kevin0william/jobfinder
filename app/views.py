from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Offre,Message,Produit,Notification,Cv
# Create your views here.


#################
#AUTHENTIFICATION
#################

def index(request):
    return render(request,'app/index.html')


def inscription(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:
            messages.error(request, "Les mots de passe ne correspondent pas.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà utilisé.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Inscription réussie ! Connectez-vous.")
            return redirect('connexion')

    return render(request, 'app/inscription.html')


def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('accueil')
        else:
            messages.error(request, "Nom d’User ou mot de passe incorrect.")

    return render(request, 'app/connexion.html')


def deconnexion(request):
    logout(request)
    return redirect('index')

@login_required
def accueil(request):
    query = request.GET.get('q')
    if query :
        offres = Offre.objects.filter(
            Q(titre__icontains=query)|
            Q(ville__icontains=query)
        ).order_by('-date_creation')
    else:
        offres = Offre.objects.all().order_by('-date_creation')
    return render(request,'app/accueil.html',{'offres':offres})

# 
    
# @login_required
# def cv(request):
#     query = request.GET.get('q')
#     if query :
#         cvs = Cv.objects.filter(
#             Q(competence__icontains=query)|
#             Q(ville__icontains=query)
#         ).order_by('-date')
#     else:
#         cvs = Cv.objects.all().order_by('-date')
#     return render(request,'app/cv.html',{'cvs':cvs})


@login_required
def creation_offre(request):
    if request.method=='POST':
        createur = request.user
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        salaire = request.POST.get('salaire')
        type_paiement= request.POST.get('type_paiement')
        image = request.FILES.get('image')
        ville = request.POST.get('ville')
        Offre.objects.create(
            createur=createur,
            titre=titre,
            description=description,
            salaire=salaire,
            type_paiement=type_paiement,
            image=image,
            ville=ville
        )
        return redirect('accueil')
    return render(request,'app/creation_offre.html')

@login_required
def produit(request):
    query = request.GET.get('q')
    if query :
        produits = Produit.objects.filter(
            Q(titre__icontains=query)|
            Q(ville__icontains=query)
        ).order_by('-date_creation')
    else:
        produits = Produit.objects.all().order_by('-date_creation')
    return render(request,'app/produit.html',{'produits':produits})


@login_required
def creation_produit(request):
    if request.method=='POST':
        createur = request.user
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        prix = request.POST.get('prix')
        image = request.FILES.get('image')
        ville = request.POST.get('ville')
        Produit.objects.create(
            createur=createur,
            nom=nom,
            description=description,
            prix=prix,
            image=image,
            ville=ville
        )
        return redirect('produit')
    return render(request,'app/creation_produit.html')


@login_required
def user_list(request):
    users = User.objects.all().order_by('email').reverse()
    return render(request,'app/utilisateur.html',{'users':users})

def discussion(request, user_id):
    receiver = User.objects.get(id=user_id)
    sender = request.user
    contenue = request.GET.get('contenue')
    if contenue :
        Message.objects.create(sender=sender,receiver=receiver,message=contenue)
        Notification.objects.create(user=receiver,envoyeur=sender,message=contenue)

    messages = Message.objects.filter(sender=sender , receiver=receiver) | Message.objects.filter(sender=receiver, receiver=sender)
    messages = messages.order_by('pk')

    if request.method == 'POST':
        message = request.POST.get('message')
        Message.objects.create(sender=sender, receiver = receiver , message=message)
        Notification.objects.create(user=receiver,envoyeur=sender,message=message)
        return redirect('discussion',user_id=user_id)

    return render(request, 'app/discussion.html', {'receiver': receiver , 'messages':messages})

def supprimer_offre(request,id):
    offre=get_object_or_404(Offre,id=id)
    offre.delete()
    return redirect('accueil')

def supprimer_produit(request,id):
    produit=get_object_or_404(Produit,id=id)
    produit.delete()
    return redirect('produit')

# def supprimer_cv(request,id):
#     cv=get_object_or_404(Cv,id=id)
#     cv.delete()
#     return redirect('cv')

def detail_offre(request,id):
    offre=get_object_or_404(Offre,id=id)
    return render(request,'app/detail_offre.html',{'offre':offre})


def detail_produit(request,id):
    produit=get_object_or_404(Produit,id=id)
    return render(request,'app/detail_produit.html',{'produit':produit})

# def detail_cv(request,id):
#     cv=get_object_or_404(Cv,id=id)
#     return render(request,'app/detail_cv.html',{'cv':cv})

@login_required
def profil_view(request):
    user = request.user

    # Récupérer les offres et produits créés par cet utilisateur
    offres = Offre.objects.filter(createur=user)
    produits = Produit.objects.filter(createur=user)

    context = {
        'user': user,
        'offres': offres,
        'produits': produits,
    }
    return render(request, 'app/profil.html', context)



@login_required
def modif_offre(request,id):
    offre = get_object_or_404(Offre,id=id)
    if request.method=='POST':
        offre.titre = request.POST.get('titre')
        offre.description = request.POST.get('description')
        offre.salaire = request.POST.get('salaire')
        offre.type_paiement= request.POST.get('type_paiement')
        offre.image = request.FILES.get('image')
        offre.ville = request.POST.get('ville')
        offre.save()
        return redirect('accueil')
    return render(request,'app/modif_offre.html',{'offre':offre})

    

@login_required
def modif_produit(request,id):
    produit = get_object_or_404(Produit,id=id)
    if request.method=='POST':
        produit.titre = request.POST.get('titre')
        produit.description = request.POST.get('description')
        produit.prix = request.POST.get('prix')
        produit.type_paiement= request.POST.get('type_paiement')
        produit.image = request.FILES.get('image')
        produit.ville = request.POST.get('ville')
        produit.save()
        return redirect('produit')
    return render(request,'app/modif_produit.html',{'produit':produit})

    
@login_required
def Notification_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-date')
    return render(request,'app/notification.html',{'notifications':notifications})

@login_required
def notif_all(request):
    users = User.objects.all()
    envoyeur = request.user
    if request.method == 'POST':
        message = request.POST.get('message')
        for user in users:
            Notification.objects.create(user=user,envoyeur=envoyeur,message=message)
        return redirect('accueil')
    return render(request,'app/notif_all.html')