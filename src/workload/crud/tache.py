from workload.models import *
from workload.forms import TacheForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView

class TacheCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Tache
	form_class = TacheForm
	template_name = "workload/tache/tache_create.html"
	success_message = "Tâche créée avec succès"

	def form_valid(self, form):
		mission = form.cleaned_data.get("mission")
		projet = form.cleaned_data.get("projet")

		if not mission and not projet:
			messages.error(self.request, "Une tâche doit être liée à une mission ou à un projet.")
			return self.form_invalid(form)

		if mission and projet:
			messages.error(self.request, "Une tâche ne peut pas être liée à la fois à une mission et à un projet.")
			return self.form_invalid(form)

		# Si c'est bon, on peut sauvegarder
		form.instance.created_by = self.request.user
		return super().form_valid(form)

	def get_success_url(self):
		next_url = self.request.GET.get("next") or self.request.POST.get("next")
		if next_url:
			return next_url
		else:
			return reverse("workload:accueil")

class TacheListView(LoginRequiredMixin, ListView):
	model = Tache
	context_object_name = "taches"
	template_name = "workload/tache/tache_list.html"

class TacheDetailView(LoginRequiredMixin, DetailView):
	model = Tache
	template_name = "workload/tache/tache_details.html"

class TacheUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	model = Tache
	form_class = TacheForm
	template_name = "workload/tache/tache_create.html"
	success_message = "Tâche modifiée avec succès"

	def get_success_url(self):
		return self.object.get_absolute_url()

class TacheDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
	model = Tache
	template_name = "warning/objet_a_effacer.html"
	success_message = "Tâche supprimée avec succès"

	def get_success_url(self):
		next_url = self.request.GET.get("next") or self.request.POST.get("next")
		if next_url:
			return next_url
		else:
			return reverse("workload:accueil")