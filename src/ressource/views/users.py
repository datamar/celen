import csv, io
from django.apps import apps
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ressource.forms.users import UserUpdateForm, ProfileUpdateForm, CustomUserCreateForm, ImportUserForm
from ressource.models.users import Profil
from ressource.models.utility import Cachet
from workload.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User, Group
from django.views.generic import ListView, CreateView, DetailView,  DeleteView

@login_required
def import_utilisateurs(request):
	if request.method == "POST":
		form = ImportUserForm(request.POST, request.FILES)
		if form.is_valid():
			fichier = form.cleaned_data["fichier"]
			decoded_file = fichier.read().decode('utf-8')
			csv_file = csv.DictReader(io.StringIO(decoded_file))
			nbr_users_importes = 0
			for row in csv_file:
				username = row.get('username')
				email = row.get('email')
				first_name = row.get('first_name', '')
				last_name = row.get('last_name', '')
				group_name = row.get("group", "").strip()
				telephone = row.get("phone", "")

				if User.objects.filter(username=username).exists():
					messages.warning(request, f"Utilisateur '{username}' déjà existant.")
					continue

				user = User.objects.create_user(
					username=username,
					email=email,
					first_name=first_name,
					last_name=last_name,
					password="silencio",
					
					#password=User.objects.make_random_password()
				)
				p = Profil.objects.get(user=user)
				p.phone = telephone
				p.save()
				if group_name:
					group, _ = Group.objects.get_or_create(name=group_name)
					user.groups.add(group)

				nbr_users_importes += 1	
			messages.success(request, f"{nbr_users_importes} utilisateurs ont été créés avec succès.")

			return redirect("workload:accueil")
	else:
		form = ImportUserForm()
	
	return render(request, "ressource/users/users_import.html", {"form": form})

class UserDetailsView(LoginRequiredMixin, DetailView):
	model = Profil
	template_name = "ressource/users/user_details.html"

class UserCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
	model = User
	form_class = CustomUserCreateForm
	template_name = "ressource/users/user_create.html"
	success_message = "L'utilisateur <strong>%(username)s</strong> a bien été créé.<br>Un courriel lui a été envoyé à l'adresse suivante: <strong>%(email)s</strong>."

	def dispatch(self, request, *args, **kwargs):
		if request.user.groups.filter(name="Utilisateur").exists():
			messages.error(request, "Vous n'avez pas la permission d'accéder à cette page.")
			return redirect('ressource:profile')
		return super().dispatch(request, *args, **kwargs)

	def get_success_url(self):
		# ?next={{ request.path }}
		return self.request.GET.get("next",reverse_lazy('ressource:users-list'))

class UsersList(LoginRequiredMixin, ListView):
	model = Profil
	template_name = "ressource/users/users_list.html"

	def dispatch(self, request, *args, **kwargs):
		if request.user.groups.filter(name="Utilisateur").exists():
			messages.error(request, "Vous n'avez pas la permission d'accéder à cette page.")
			return redirect('ressource:accueil')
		return super().dispatch(request, *args, **kwargs)

@login_required
def profile(request):
	profil = request.user.profile
	if request.method == "POST":
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, 'Vos informations ont été mises à jour.')
			return redirect('ressource:profile')
	else:        
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	# historique des activités
	all_objects = []	
	for model in apps.get_models():
		if issubclass(model,Cachet) and not model._meta.abstract:
			queryset = model.objects.all()
			all_objects.extend(queryset)
	historique = sorted(all_objects, key=lambda x: x.modified, reverse=True)
	users = User.objects.all()
	#missions = Mission.objects.all().order_by("nom")
	#projets = Projet.objects.all().order_by("modified")
	context = {
		"historique":historique,
		'u_form':u_form,
		'p_form':p_form,
		"profil":profil,
		"users":users,
		#"missions":missions,
		#"projets":projets
	}
	return render(request, 'ressource/users/profile.html', context)