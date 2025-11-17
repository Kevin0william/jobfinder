from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator

# Create your models here.



class Offre(models.Model):
    TYPE = [('jour','Par jour'),
            ('semaine','Par semaine'),
            ('mois','Par mois'),
            ]
    createur = models.ForeignKey(User,on_delete=models.CASCADE)
    titre = models.CharField(max_length=150)
    description = models.TextField()
    salaire = models.PositiveIntegerField(null=True)
    type_paiement = models.CharField(max_length=10,choices=TYPE,default='mois')
    ville = models.CharField(max_length=100)
    image = models.ImageField(upload_to='offres/images/',null=True,blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User,related_name='offre_likee',blank=True)
    def __str__(self):
        return self.titre
    @property
    def total_like(self):
        return self.likes.count()


class Produit(models.Model):
    createur = models.ForeignKey(User,on_delete=models.CASCADE)
    nom = models.CharField(max_length=150)
    description = models.TextField()
    prix = models.PositiveIntegerField()
    ville = models.CharField(max_length=100)
    image = models.ImageField(upload_to='offres/images/',null=True,blank=True)
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nom
    


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE , related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE , related_name='receiver')
    message = models.TextField()
    date=models.DateTimeField(default=timezone.now)


class Notification(models.Model):
    envoyeur = models.ForeignKey(User,on_delete=models.CASCADE , related_name='envoyeur' , null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE , related_name='user')
    # message = models.ForeignKey(Message,on_delete=models.CASCADE)
    message = models.TextField()
    date=models.DateTimeField(default=timezone.now)


class Cv(models.Model):
    createur = models.ForeignKey(User,on_delete=models.CASCADE)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    competence = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField()
    experience= models.PositiveIntegerField()
    pays = models.CharField(max_length=100,null=True)
    ville = models.CharField(max_length=100,null=True)
    image = models.ImageField(upload_to='offres/images/',blank=True,null=True)
    date= models.DateTimeField(default=timezone.now)


class Boost(models.Model):
    createur = models.ForeignKey(User,on_delete=models.CASCADE)
    nom = models.CharField(max_length=150)
    lien = models.URLField(unique=True)
    
    def str(self):
        self.nom


class suivi(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    boost = models.ForeignKey(Boost,on_delete=models.CASCADE)
    date= models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user','boost')

class Createur(models.Model):
    nom = 'MATIP YAB'
    prenom = 'Kevin Dieudonne'
    date_naissance = '04/03/2006'
    date_creation_jobfinder = 'octobre 2025'


class Publication(models.Model):
    STYLE_CHOICES = [
        ('style1','Style1'),
        ('style2','Style2'),
        ('style3','Style3'),
        ('style4','Style4'),
        ('style5','Style5'),
        ('style6','Style6'),
        ('style7','Style7'),
        ('style8','Style8'),
        ('style9','Style9'),
        ('style10','Style10'),
    ]
    createur = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField(null=True,blank=True)
    style = models.CharField(max_length=20,choices=STYLE_CHOICES)
    date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User,related_name='like_publication',blank=True)
    
    def __str__(self):
        return self.message

    def total_likes(self):
        return self.likes.count()
    
    
        
class Commentaire(models.Model):
    publication = models.ForeignKey(Publication,on_delete=models.CASCADE, related_name="commentaires")
    createur = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User,related_name='like_commentaire',blank=True)
    
    def total_likes(self):
        return self.likes.count()

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[("user","Utilisateur"),("assistant","Lia")])
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.user.username} ({self.role}): {self.content[:50]}"
