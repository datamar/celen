from workload.models import *
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from workload.forms import ImplicationForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView

class ImplicationDetailView(LoginRequiredMixin, DetailView):
	model = Implication
	template_name = "workload/implication/implication_details.html"

class ImplicationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Implication
	form_class = ImplicationForm
	template_name = "workload/implication/implication_create.html"

	def get(self, request, *args, **kwargs):
		response = super().get(request, *args, **kwargs)
		response["Content-Type"] = "text/html; charset=utf-8"
		return response

	def dispatch(self, request, *args, **kwargs):
		self.content_type = get_object_or_404(
			ContentType, id=kwargs["content_type_id"]
		)
		self.target_object = get_object_or_404(
			self.content_type.model_class(), id=kwargs["object_id"]
		)
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		implication = form.save(commit=False)
		implication.content_type = self.content_type
		implication.object_id = self.target_object.id
		implication.created_by = self.request.user
		try:
			implication.save()
			messages.success(self.request, "Implication ajoutée avec succès.")
		except IntegrityError:
			messages.error(self.request, f"{implication.agent} est déjà impliqué dans cet élément.")
		response = redirect(self.target_object.get_absolute_url())
		return response

	def get_success_url(self):
		next_url = self.request.GET.get("next") or self.request.POST.get("next")
		if next_url:
			return next_url
		else:
			return redirect("ressource:profile")

class ImplicationUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	model = Implication
	form_class = ImplicationForm
	template_name = "workload/implication/implication_create.html"
	success_message = "Modifications de la charge de travail enregistrées."

	def get_success_url(self):
		next_url = self.request.GET.get("next") or self.request.POST.get("next")
		if next_url:
			return next_url
		else:
			return self.object.cible.get_absolute_url()

class ImplicationListView(LoginRequiredMixin, ListView):
	model = Implication
	template_name = "workload/implication/implication_list.html"

class ImplicationDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
	model = Implication
	template_name = "warning/desengagement.html"
	success_message = "Modifications de la charge de travail enregistrées."

	def get_success_url(self):
		next_url = self.request.GET.get("next") or self.request.POST.get("next")
		if next_url:
			return next_url
		else:
			return redirect("ressource:profile")