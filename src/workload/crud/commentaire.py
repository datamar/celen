from workload.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from workload.forms import CommentaireForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView

class CommentaireDetailView(LoginRequiredMixin, DetailView):
	model = Commentaire
	template_name = "workload/commentaire/commentaire_details.html"

class CommentaireCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Commentaire
	form_class = CommentaireForm
	template_name = "workload/commentaire/commentaire_create.html"
	success_message = "Commentaire bien noté !"

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
		commentaire = form.save(commit=False)
		commentaire.content_type = self.content_type
		commentaire.object_id = self.target_object.id
		commentaire.created_by = self.request.user
		commentaire.save()
		response = redirect(self.target_object.get_absolute_url())
		return response

class CommentaireUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	model = Commentaire	
	form_class = CommentaireForm
	template_name = "workload/commentaire/commentaire_create.html"
	success_message = "Commentaire modifié"

	def get_success_url(self):
		return self.object.cible.get_absolute_url()

class CommentaireDeleteView(LoginRequiredMixin, SuccessMessageMixin,  DeleteView):
	model = Commentaire
	template_name = "warning/objet_a_effacer.html"
	success_message = "Commentaire bien effacé !"

	def get_success_url(self):
		return self.object.cible.get_absolute_url()

class CommentaireListView(LoginRequiredMixin, ListView):
	model = Commentaire
	template_name = "workload/commentaire/commentaire_list.html"
