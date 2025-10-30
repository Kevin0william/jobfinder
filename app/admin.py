from django.contrib import admin
from .models import Message,Offre,Produit,Notification,Cv,Boost
# Register your models here.

class OffreAdmin(admin.ModelAdmin):
    list_display=('createur','titre','description','salaire','type_paiement','ville','image','date_creation')
    search_fields = ['titre','ville','createur__username']

admin.site.register(Offre,OffreAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display=('sender','receiver','message','date')

admin.site.register(Message,MessageAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display=('envoyeur','user','message','date')

admin.site.register(Notification,NotificationAdmin)


class ProduitAdmin(admin.ModelAdmin):
    list_display=('createur','nom','description','prix','ville','image','date_creation')

admin.site.register(Produit,ProduitAdmin)

class AdminCv(admin.ModelAdmin):
    list_display=('createur','prenom','nom','email','telephone','competence','description','experience','ville','image','date')
    search_fields=['createur__username','competence']

admin.site.register(Cv,AdminCv)

class BoostAdmin(admin.ModelAdmin):
    list_display=('Createur','nom','lien','suivre','boost_id')

admin.site.register(Boost,BoostAdmin)