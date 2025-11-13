from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
# import openai
# from openai import OpenAI
from pro.settings import GPT4_API_KEY
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Offre,Message,Produit,Notification,Cv,Boost,suivi,Publication,Commentaire,ChatMessage

# Create your views here.

####################################################################
##
### AUTHENTIFICATON
##
####################################################################

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

####################################################################
##
### ACCES
##
####################################################################

def index(request):
    return render(request,'app/index.html')

@login_required
def accueil(request):
    query = request.GET.get('q')
    if query :
        offres = Offre.objects.filter(
            Q(createur__icontains=query)|
            Q(titre__icontains=query)|
            Q(ville__icontains=query)
        ).order_by('-date_creation')
    else:
        offres = Offre.objects.all().order_by('-date_creation')
        s=0
        for offre in offres:
            if offre.createur == request.user :
                s += offre.total_like
    return render(request,'app/accueil.html',{'offres':offres,'s':s})
    
@login_required
def cv(request):
    query = request.GET.get('q')
    if query :
        cvs = Cv.objects.filter(
            Q(prenom__icontains=query)|
            Q(nom__icontains=query)|
            Q(competence__icontains=query)|
            Q(pays__icontains=query)|
            Q(ville__icontains=query)
        ).order_by('-date')
    else:
        cvs = Cv.objects.all().order_by('-date')
    return render(request,'app/cv.html',{'cvs':cvs})

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
def Notification_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-date')
    return render(request,'app/notification.html',{'notifications':notifications})

@login_required
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

@login_required
def user_list(request):
    users = User.objects.all().order_by('email').reverse()
    return render(request,'app/utilisateur.html',{'users':users})

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

def options_avance(request):
    likes_p = Publication.objects.all()
    likes_o = Offre.objects.all()
    s1=0
    s2=0
    s=0
    for like_o in likes_o:
        if like_o.createur == request.user :
            s1 += like_o.total_like
    for like_p in likes_p:
        if like_p.createur == request.user :
            s2 += like_p.likes.count()
    
    s += s1 + s2
    return render(request,'app/options_avance.html',{'s':s})

def publication(request):
    publics = Publication.objects.all().order_by('-date')
    return render(request,'app/publication.html',{'publics':publics})

####################################################################
##
### CREATION
##
####################################################################

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
def creation_cv(request):
    if request.method == 'POST':
        createur = request.user
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        age = request.POST.get('age')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        competence = request.POST.get('competence')
        description = request.POST.get('description')
        experience = request.POST.get('experience')
        pays = request.POST.get('pays')
        ville = request.POST.get('ville')
        Cv.objects.create(
            createur=createur,
            nom=nom,
            prenom=prenom,
            age=age,
            email=email,
            telephone=telephone,
            competence=competence,
            description=description,
            experience=experience,
            pays=pays,
            ville=ville,
            )
        return redirect('cv')
    return render(request,'app/creation_cv.html')

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
def notif_all(request):
    users = User.objects.all()
    envoyeur = request.user
    if request.method == 'POST':
        message = request.POST.get('message')
        for user in users:
            Notification.objects.create(user=user,envoyeur=envoyeur,message=message)
        return redirect('accueil')
    return render(request,'app/notif_all.html')

@login_required
def creation_publication(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        style = request.POST.get('style')
        if message and style:
            Publication.objects.create(
                createur = request.user,
                message = message,
                style = style
            )
            return redirect('publication')
    return render(request,'app/creation_publication.html')

@login_required
def commentaires_view(request, id):
    publication = get_object_or_404(Publication, id=id)
    commentaires = publication.commentaires.all().order_by('-date')

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            Commentaire.objects.create(
                publication=publication,
                createur=request.user,
                message=message
            )
            return redirect('commentaires', id=id)

    return render(request, 'app/commentaires.html', {
        'publication': publication,
        'commentaires': commentaires,
    })


####################################################################
##
### SUPPRESSION
##
####################################################################

def supprimer_offre(request,id):
    offre=get_object_or_404(Offre,id=id)
    offre.delete()
    return redirect('accueil')

def supprimer_produit(request,id):
    produit=get_object_or_404(Produit,id=id)
    produit.delete()
    return redirect('produit')

def supprimer_cv(request,id):
    cv=get_object_or_404(Cv,id=id)
    cv.delete()
    return redirect('cv')

def supprimer_publication(request,id):
    pub = get_object_or_404(Publication,id=id)
    pub.delete()
    return redirect('publication')

####################################################################
##
### DETAIL
##
####################################################################

def detail_cv(request,id):
    cv=get_object_or_404(Cv,id=id)
    return render(request,'app/detail_cv.html',{'cv':cv})

def detail_offre(request,id):
    offre=get_object_or_404(Offre,id=id)
    return render(request,'app/detail_offre.html',{'offre':offre})

def detail_produit(request,id):
    produit=get_object_or_404(Produit,id=id)
    return render(request,'app/detail_produit.html',{'produit':produit})

####################################################################
##
### MODIFIER
##
####################################################################

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
def modif_cv(request,id):
    cv = get_object_or_404(Cv,id=id)
    if request.method=='POST':
        cv.nom = request.POST.get('nom')
        cv.prenom = request.POST.get('prenom')
        cv.age = request.POST.get('age')
        cv.email = request.POST.get('email')
        cv.competence = request.POST.get('competence')
        cv.description = request.POST.get('description')
        cv.experience = request.POST.get('experience')
        cv.pays = request.POST.get('pays')
        cv.ville = request.POST.get('ville')
        cv.save()
        return redirect('cv')
    return render(request,'app/modif_cv.html',{'cv':cv})

def modifier_publication(request,id):
    publication = get_object_or_404(Publication,id=id)
    if request.method == 'POST':
        publication.message = request.POST.get('message')
        publication.style = request.POST.get('style')
        publication.save()
        return redirect('publication')
    return render(request,'app/modifier_publication.html')

####################################################################
##
### SURPLUS
##
####################################################################

def add_page(request):
    if request.method == 'POST':
        createur = request.user
        nom = request.POST.get('nom')
        lien = request.POST.get('lien')
        if Boost.objects.filter(lien=lien):
            messages.error(request,'Une page a deja ete presenter avec ce lien')
        else:
            Boost.objects.create(
                createur=createur,
                nom=nom,
                lien=lien,
            )
            return redirect('boost_page')
    return render(request,'app/add_page.html')

def boost_page(request):
    pages = Boost.objects.all()
    suivis = suivi.objects.filter(user=request.user).values_list('boost_id',flat=True)
    return render(request,'app/boost_page.html',{'pages':pages,'suivis':suivis})

def suivre(request,id):
    page = get_object_or_404(Boost,id=id)
    suivi.objects.get_or_create(user=request.user,boost=page)
    return redirect(page.lien)

def like_offre(request,offre_id):
    offre = get_object_or_404(Offre,id=offre_id)
    user = request.user
    if user in offre.likes.all():
        offre.likes.remove(user)
    else:
        offre.likes.add(user)
    return redirect('accueil')

def like_publication(request,publication_id):
    publication = get_object_or_404(Publication,id=publication_id)
    user = request.user
    if user in publication.likes.all():
        publication.likes.remove(user)
    else:
        publication.likes.add(user)
    return redirect('publication')


def total(request):
    offres = Offre.objects.filter(createur = request.user)
    for offre in offres:
        likes = offre.likes.all()
    return render(request,'app/accueil.html',{'likes':likes})
def total_p(request):
    publications = Publication.objects.filter(createur = request.user)
    for pub in publications:
        likes = pub.likes.all()
    return render(request,'app/publication.html',{'likes':likes})
            

# client = OpenAI(api_key=GPT4_API_KEY)

# openai.api_key = GPT4_API_KEY

# @login_required
# def chat_with_lia(request):
#     chats = ChatMessage.objects.filter(user=request.user)
#     if request.method == "POST":
#         message = request.POST.get("message", "").strip()
#         ChatMessage.objects.create(
#             user = request.user,
#             role = 'user',
#             content = message
#         )
#         if not message:
#             return JsonResponse({'response': 'Message vide'}, status=400)
        
#         # Historique limité aux 100 derniers messages
#         history = request.session.get('chat_history', [])
#         history.append({"role": "user", "content": message})
#         history = history[-100:]  # garde seulement les 100 derniers

#         # Vérifier si le message est une salutation simple
#         salutations = ['salut', 'bonjour', 'hello', 'coucou', 'hi','cc','yo']
#         if message.lower() in salutations:
#             reply = f"Salut {request.user}! Comment puis-je vous aider ?"
#             ChatMessage.objects.create(
#             user = request.user,
#             role = 'assistant',
#             content = reply
#             )
#         else:
#     # Construire le prompt avec l'historique de manière concise
#             full_prompt = """
#                     Tu es JobFinder, l’assistant officiel de la plateforme numérique JobFinder.
#                     Tu dois répondre de manière simple, brève et précise, en allant directement à l’essentiel.
#                     Tu réponds uniquement à la question posée, sans ajouter d’informations inutiles.
#                     Tu essaie toujours de creer un espace de confiance entre les utilisateurs et toi

#                     Voici ce que tu dois savoir :

#                     📌 À propos de JobFinder :
#                     - Plateforme numérique pour trouver un emploi et vendre des services/produits en Afrique.
#                     - Mission : aider la communauté à trouver facilement du travail et valoriser les compétences.
#                     - Les utilisateurs peuvent publier des offres, des CV et des annonces visibles par tous.

#                     📌 Fonctionnalités clés :
#                     1. Likes :
#                     - Les likes viennent des offres et des publications.
#                     - Ils servent au système de récompense.

#                     2. Système de Récompense :
#                     - À 1000 likes → l’utilisateur gagne 5 $.
#                     - Après chaque récompense, le quota augmente de +1000 likes pour obtenir les 5 $ suivants.
#                     - Exemple : 1000 ✅ → 5 $ | 2000 ✅ → 5 $ | 3000 ✅ → 5 $
#                     - Le quota de like avant une recompense augmente mais pas la recompense

#                     3. Recherche :
#                     - Sur la page d’accueil et la page CV :
#                     - On peut rechercher par titre, ville ou nom du créateur.
#                     - Pour annuler la recherche → envoyer un champ vide.

#                     📌 Style de réponse attendu :
#                     - Toujours clair, direct, et court.
#                     - Répond toujours uniquement à la question posée.
#                     - Pas d'informations non demandées.
#                     - Donne ton avis personnel si l'utilisateur te pose une question de logique.
#                     - Reponse amicale mais professionel

#                     Tu as une parfaite connaissance du fonctionnement de la plateforme JobFinder.
#                     Mais tu connais egalement d'autre sujet sur la vie , le monde et bien d'autre donc si l'utilisateur te demande une histoire , de jouer ou simplement de discuter tu peux le faire sans introduire d'information sur la plateforme JobFinder.

#                     Réponds maintenant à la question de l’utilisateur :
#                     """

#             for msg in history[-20:]:  # garder seulement les 20 derniers pour la fluidité
#                 full_prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"


#             try:
#                 response = client.responses.create(
#                     model="gpt-5-nano",
#                     input=full_prompt,
#                     store=True,
#                 )
#                 reply = response.output_text.strip()
#                 ChatMessage.objects.create(
#                     user = request.user,
#                     role = 'Lia',
#                     content = reply
#                     )
#             except Exception as e:
#                 return JsonResponse({'response': f'Erreur : {str(e)}'}, status=500)

#         # Ajouter la réponse de l'IA dans l'historique
#         history.append({"role": "assistant", "content": reply})
#         request.session['chat_history'] = history[-100:]  # limite mémoire à 100 messages

#         return JsonResponse({'response': reply})
    
#     return render(request, "app/chat_lia.html",{'chats':chats})




def total_like_offre(request):
    user = request.user
    offres = Offre.objects.filter(createur=user)
    total_likes = sum(offre.likes.count() for offre in offres)
    if total_likes == 1000:
        messages.success(request,'Felicitation ! Vous avez recu 1000 likes.')
    context = {
        'total_likes':total_likes,
    }
    return render(request,'app/profil.html',context)