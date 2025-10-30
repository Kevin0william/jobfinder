from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.index , name='index'),
    path('inscription/',views.inscription, name='inscription'),
    path('connexion/',views.connexion , name='connexion'),
    path('accueil/',views.accueil , name='accueil'),
    path('deconnexion/',views.deconnexion , name='deconnexion'),
    path('creation_offre/',views.creation_offre , name='creation_offre'),
    path('produit/',views.produit , name='produit'),
    path('creation_produit/',views.creation_produit , name='creation_produit'),
    path('user_list/',views.user_list, name='user_list'),
    path('discussion/<int:user_id>/',views.discussion, name='discussion'),
    path('supprimer_offre/<int:id>/',views.supprimer_offre, name='supprimer_offre'),
    path('detail_offre/<int:id>/',views.detail_offre, name='detail_offre'),
    path('detail_produit/<int:id>/',views.detail_produit, name='detail_produit'),
    # path('detail_cv/<int:id>/',views.detail_cv, name='detail_cv'),
    path('supprimer_produit/<int:id>/',views.supprimer_produit, name='supprimer_produit'),
    # path('supprimer_cv/<int:id>/',views.supprimer_cv, name='supprimer_cv'),
    path('profil/', views.profil_view, name='profil'),
    # path('cv/', views.cv, name='cv'),
    # path('creation_cv/', views.creation_cv, name='creation_cv'),
    path('modif_offre/<int:id>', views.modif_offre, name='modif_offre'),
    path('modif_produit/<int:id>', views.modif_produit, name='modif_produit'),
    path('notification/',views.Notification_view,name='notification'),
    path('notif_all/',views.notif_all,name='notif_all'),
    path('add_page/',views.add_page,name='add_page'),
    path('boost_page/',views.boost_page,name='boost_page'),
    path('suivre/<int:id>',views.suivre,name='suivre'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)