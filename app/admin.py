from django.contrib import admin
from .models import Message,Offre,Produit,Notification,Cv,Boost,suivi,Createur,Publication,Commentaire,ChatMessage
# Register your models here.

class OffreAdmin(admin.ModelAdmin):
    list_display=('createur','titre','description','salaire','type_paiement','ville','image','date_creation','nombre_likes')
    search_fields = ['titre','ville','createur__username']
    def nombre_likes(self,obj):
        return obj.likes.count()
    nombre_likes.short_description = 'Likes'

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

@admin.register(Cv)
class AdminCv(admin.ModelAdmin):
    list_display=('createur','prenom','nom','age','email','telephone','competence','description','experience','pays','ville','image','date','createur_id')
    search_fields=['createur__username','competence']

# admin.site.register(Cv,AdminCv)

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display=('createur','message','nombre_likes')

    def nombre_likes(self,obj):
        return obj.likes.count()
    nombre_likes.short_description = 'Likes'

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display=('createur','message','nombre_likes')

    def nombre_likes(self,obj):
        return obj.likes.count()
    nombre_likes.short_description = 'Likes'

class BoostAdmin(admin.ModelAdmin):
    list_display=('createur','nom','lien')

admin.site.register(Boost,BoostAdmin)

class suiviAdmin(admin.ModelAdmin):
    list_display=('user','boost__nom','date')

admin.site.register(suivi,suiviAdmin)

class CreateurAdmin(admin.ModelAdmin):
    list_display=('nom','prenom','date_naissance','date_creation_jobfinder')
    def has_add_permission(self, request):
        if Createur.objects.count() >= 1:
            return False
        return True
    
admin.site.register(Createur,CreateurAdmin)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display=('user','role','content','date')