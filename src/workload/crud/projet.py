from workload.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from workload.forms import ProjetForm
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView

class ProjetDetailView(LoginRequiredMixin, DetailView):
	model = Projet
	template_name = "workload/projet/projet_details.html"

class ProjetListView(LoginRequiredMixin, ListView):
    model = Projet
    template_name = "workload/projet/projet_list.html"

class ProjetCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Projet
	form_class = ProjetForm
	template_name = "workload/projet/projet_create.html"
	success_message = "Projet créé avec succès !"

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super().form_valid(form)

	def get_success_url(self):
		next_url = self.request.GET.get("next") or self.request.POST.get("next")
		if next_url:
			return next_url
		else:
			return reverse("ressource:profile")

class ProjetUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	model = Projet
	form_class = ProjetForm
	template_name = "workload/projet/projet_create.html"
	success_message = "Projet modifié avec succès"

	def form_valid(self, form):
		form.instance.modified_by = self.request.user
		return super().form_valid(form)

class ProjetDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
	model = Projet
	template_name = "warning/objet_a_effacer.html"
	success_message = "Projet supprimé avec succès"
