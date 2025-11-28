from workload.models import *
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView

class MissionDetailView(LoginRequiredMixin, DetailView):
	model = Mission
	template_name = "workload/mission/mission_details.html"

class MissionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Mission
	fields = ["nom", "description", "tags"]
	template_name = "workload/mission/mission_create.html"
	success_message = "Mission créée avec succès"

	def get_success_url(self):
		next_url = self.request.GET.get("next") or self.request.POST.get("next")
		if next_url:
			return next_url
		else:
			return reverse("ressource:profile")

class MissionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	model = Mission
	fields = ["nom","description","tags"]
	template_name = "workload/mission/mission_create.html"
	success_message = "Mission modifiée avec succès"

class MissionListView(LoginRequiredMixin, ListView):
	model = Mission
	template_name = "workload/mission/missions_list.html"

	def get_queryset(self):
		return Mission.objects.prefetch_related(
			'documents', 
			'commentaires',
			'implications',
			'tags'
		).order_by('-created')

class MissionDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
	model = Mission
	template_name = "warning/objet_a_effacer.html"
	success_message = "Mission supprimée avec succès"

	def get_success_url(self):
		next_url = self.request.GET.get("next") or self.request.POST.get("next")
		if next_url:
			return next_url
		else:
			return reverse("ressource:profile")