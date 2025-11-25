from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from workload.models import *
from workload.forms import DocumentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DeleteView

class DocumentListView(LoginRequiredMixin, ListView):
	model = Document
	template_name = "workload/document/document_list.html"
	ordering = ("-created")

	def get_queryset(self):
		return Document.objects.prefetch_related(
			"mission_documents", "projet_documents", "livrable_documents"
		)

class DocumentDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
	model = Document
	template_name = 'warning/objet_a_effacer.html'
	success_message = "Document supprimé avec succès"
	
	def get_success_url(self):
		next_url = self.request.GET.get("next") or self.request.POST.get("next")
		if next_url:
			return next_url
		else:
			return redirect("workload:accueil")

@login_required
def document_update(request, pk):
	doc = get_object_or_404(Document, pk=pk)
	if request.method == "POST":
		form = DocumentForm(request.POST, instance=doc)
		if form.is_valid():
			# Sauvegarder les modifications
			updated_document = form.save(commit=False)
			updated_document.modified_by = request.user
			updated_document.save()			
			messages.success(request, f"Document '{updated_document.nom}' modifié avec succès")
			# Rediriger vers la page précédente ou une page par défaut
			next_url = request.GET.get("next") or request.POST.get("next")
			if next_url:
				return redirect(next_url)
			else:
				return redirect("workload:accueil")
	else:
		form = DocumentForm(instance=doc)
	
	context = {
		'form': form,
		'document': doc,
		'title': f"Modifier le document - {doc.nom}"
	}
	return render(request, 'workload/document/document_create.html', context)

@login_required
def document_create(request, content_type_id, object_id):
	# Récupérer l'objet cible
	content_type = get_object_or_404(ContentType, pk=content_type_id)
	target_object = get_object_or_404(content_type.model_class(), pk=object_id)	
	if request.method == 'POST':
		form = DocumentForm(request.POST)
		if form.is_valid():
			# Créer le document
			document = form.save(commit=False)
			document.created_by = request.user
			document.save()            
			# Associer à l'objet cible
			target_object.documents.add(document)            
			messages.success(request, f"Document '{document.nom}' ajouté à {target_object.nom}")
			next_url = request.GET.get("next") or request.POST.get("next")
			if next_url:
				return redirect(next_url)
			else:
				return redirect(target_object.get_absolute_url())
	else:
		form = DocumentForm()	
	context = {
		'form': form,
		'target_object': target_object,
		'content_type': content_type,
	}
	return render(request, 'workload/document/document_create.html', context)