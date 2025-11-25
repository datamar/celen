from workload.models import *
from workload.forms import LivrableForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView

class LivrableListView(LoginRequiredMixin, ListView):
    model = Livrable
    template_name = "workload/livrable/livrable_list.html"
    context_object_name = "livrables"

class LivrableCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Livrable
    form_class = LivrableForm
    template_name = "workload/livrable/livrable_create.html"
    success_message = "Livrable créé avec succès"

    def get_success_url(self):
        # si next= est fourni dans l’URL, on le suit
        next_url = self.request.GET.get("next") or self.request.POST.get("next")
        if next_url:
            return next_url
        return reverse("workload:livrable_details", kwargs={"pk": self.pk})

class LivrableUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Livrable
    form_class = LivrableForm
    template_name = "workload/livrable/livrable_create.html"
    success_message = "Livrable mis à jour avec succès"


class LivrableDetailView(LoginRequiredMixin, DetailView):
    model = Livrable
    template_name = "workload/livrable/livrable_details.html"

class LivrableDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Livrable
    template_name = "warning/objet_a_effacer.html"
    success_message = "Livrable supprimé avec succès"

    def get_success_url(self):
        # si next= est fourni dans l’URL, on le suit
        next_url = self.request.GET.get("next") or self.request.POST.get("next")
        if next_url:
            return next_url
        return reverse("workload:livrable_details", kwargs={"pk": self.pk})
