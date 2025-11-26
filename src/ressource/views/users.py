import io, csv
from django.apps import apps
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from ressource.models.users import Profil
from ressource.models.utility import Cachet
from workload.views import get_objects_grouped
from workload.models import Mission, Projet, Document, Commentaire, Tache, Livrable, Implication
from django.views.generic import ListView, CreateView, DetailView
from ressource.forms import UserUpdateForm, ProfileUpdateForm, CustomUserCreateForm, ImportUserForm, ImplicationForm

@login_required
def profile(request):
	user = request.user
	profil = user.profile
	implications = Implication.objects.filter(agent=user)
	if request.method == "POST":
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		imp_forms = [
			ImplicationForm(request.POST, instance=imp, prefix=f"imp_{imp.pk}")
			for imp in implications
		]
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, 'Votre profil a été mis à jour.')
			return redirect('ressource:profile')
		if all(f.is_valid() for f in imp_forms):
			total_contribution = sum(
				f.cleaned_data.get("contribution", 0)
				for f in imp_forms
			)
			if total_contribution > 100:
				messages.error(request, f"Contributions cumulées trop élevées : {total_contribution}%")
			else:
				for f in imp_forms:
					if f.has_changed():
						f.save()
				messages.success(request, 'Vos implications ont été mises à jour.')
			return redirect('ressource:profile')
	else:
		u_form = UserUpdateForm(instance=user)
		p_form = ProfileUpdateForm(instance=profil)
		imp_forms = [
			ImplicationForm(instance=imp, prefix=f"imp_{imp.pk}")
			for imp in implications
		]

	context = {
		'u_form': u_form,
		'p_form': p_form,
		'implication_forms': imp_forms,
		"profil": profil,
		"users": User.objects.all(),
		"mon_activite": get_objects_grouped(user),
		"missions": Mission.objects.all(),
		"projets": Projet.objects.all(),
		"documents": Document.objects.all(),
		"commentaires": Commentaire.objects.all(),
		"taches": Tache.objects.all(),
		"livrables": Livrable.objects.all(),
		"working_agent": Implication.objects.select_related("agent").order_by("agent"),
	}
	return render(request, 'ressource/users/profile.html', context)

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

			return redirect("ressource:profile")
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
