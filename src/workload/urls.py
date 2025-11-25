from django.urls import path
from workload.views import index
from workload.crud.mission import *
from workload.crud.document import *
from workload.crud.projet import *
from workload.crud.commentaire import *
from workload.crud.tache import *
from workload.crud.livrable import *
from workload.crud.implication import *

app_name = 'workload'

urlpatterns = [
    path('', index, name='accueil'),
    # IMPLICATIONS #
    path("implications/", ImplicationListView.as_view(), name="implication_list"),
    path("implication/ajouter/<int:content_type_id>/<int:object_id>/", ImplicationCreateView.as_view(), name="implication_create"),
    path("implication/<int:pk>/modifier/", ImplicationUpdateView.as_view(), name="implication_edit"),
    path("implication/<int:pk>/supprimer/", ImplicationDeleteView.as_view(), name="implication_delete"),
    # LIVRABLES #
    path("livrables/", LivrableListView.as_view(), name="livrable_list"),
    path("livrables/nouveau/", LivrableCreateView.as_view(), name="livrable_create"),
    path("livrables/<int:pk>/", LivrableDetailView.as_view(), name="livrable_details"),
    path("livrables/<int:pk>/modifier/", LivrableUpdateView.as_view(), name="livrable_update"),
    path("livrables/<int:pk>/supprimer/", LivrableDeleteView.as_view(), name="livrable_delete"),
    # TACHES #
    path("taches/", TacheListView.as_view(), name="tache_list"),
    path("taches/create/", TacheCreateView.as_view(), name="tache_create"),
    path("taches/<int:pk>/", TacheDetailView.as_view(), name="tache_details"),
    path("taches/<int:pk>/edit/", TacheUpdateView.as_view(), name="tache_update"),
    path("taches/<int:pk>/delete/", TacheDeleteView.as_view(), name="tache_delete"),    
    # COMMENTAIRES #
    path("commentaires/", CommentaireListView.as_view(), name="commentaire_list"),
    path("commentaire/ajouter/<int:content_type_id>/<int:object_id>/", CommentaireCreateView.as_view(), name="commentaire_create"),
    path("commentaire/<int:pk>/modifier/", CommentaireUpdateView.as_view(), name="commentaire_update"),
    path("commentaire/<int:pk>/supprimer/", CommentaireDeleteView.as_view(), name="commentaire_delete"),
    path("commentaire/<int:pk>/details/", CommentaireDetailView.as_view(), name="commentaire_details"),
    # PROJETS #
    path("projets/", ProjetListView.as_view(), name="projet_list"),
    path("projet/<int:pk>/", ProjetDetailView.as_view(), name="projet_details"),
    path("projet/ajouter/", ProjetCreateView.as_view(), name="projet_create"),
    path("projet/<int:pk>/modifier/", ProjetUpdateView.as_view(), name="projet_update"),
    path("projet/<int:pk>/supprimer/", ProjetDeleteView.as_view(), name="projet_delete"),
    # DOCUMENTS #
    path("documents/", DocumentListView.as_view(), name="documents_list"),
    path('document/ajouter/<int:content_type_id>/<int:object_id>/', document_create, name='document_create'),
    path('document/<int:pk>/modifier/', document_update, name='document_update'),
    path('document/<int:pk>/effacer/', DocumentDeleteView.as_view(), name='document_delete'),
    # MISSIONS #
    path("missions/", MissionListView.as_view(), name="missions_list"),
    path("mission/<int:pk>/details/", MissionDetailView.as_view(), name="mission_details"),
    path("mission/<int:pk>/effacer/", MissionDeleteView.as_view(), name="mission_delete"),
    path("mission/creation/", MissionCreateView.as_view(), name="mission_create"),
    path("mission/<int:pk>/modifier/", MissionUpdateView.as_view(), name="mission_update"),
]