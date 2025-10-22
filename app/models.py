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
    salaire = models.PositiveIntegerField()
    type_paiement = models.CharField(max_length=10,choices=TYPE,default='mois')
    ville = models.CharField(max_length=100)
    image = models.ImageField(upload_to='offres/images/',null=True,blank=True)
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titre


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
    email = models.EmailField()
    telephone = models.CharField(max_length=9,validators=[RegexValidator(r'^\d{8,9}$',message='Numero invalide')])
    competence = models.CharField(max_length=100)
    description = models.TextField()
    experience= models.PositiveIntegerField()
    ville = models.CharField(max_length=100,null=True)
    image = models.ImageField(upload_to='offres/images/',blank=True,null=True)
    date= models.DateTimeField(default=timezone.now)
