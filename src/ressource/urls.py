from django.urls import path
from ressource.views.utility import index
from ressource.views.users import *

app_name = 'ressource'

urlpatterns = [
    path('', index, name='accueil'),
	# PROFIL #
	path("profil/", profile, name="profile"),
    # USERS #
    path('user/add/', UserCreateView.as_view(), name="new-user"),
    path('user/<int:pk>/', UserDetailsView.as_view(), name="user-details"),
    path('users/', UsersList.as_view(), name="users-list"),
    path("users/import/", import_utilisateurs, name="users-import"),
    # PROBLEME REPORT #
    path('signaler-un-bug/', signaler_bug, name='signaler_bug')

]