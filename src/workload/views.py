from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from workload.models import *

def get_objects_grouped(user):
	data = {
		"missions": set(),
		"projets": set(),
		"livrables": set(),
		"taches": set(),
	}
	# 1. via Implication
	for imp in Implication.objects.filter(agent=user):
		obj = imp.cible
		if isinstance(obj, Mission):
			data["missions"].add(obj)
		elif isinstance(obj, Projet):
			data["projets"].add(obj)
		elif isinstance(obj, Livrable):
			data["livrables"].add(obj)
		elif isinstance(obj, Tache):
			data["taches"].add(obj)
			
	# 2. via responsabilités directes (Projets, Livrables)
	data["projets"].update(Projet.objects.filter(r1=user))
	data["projets"].update(Projet.objects.filter(r2=user))
	data["livrables"].update(Livrable.objects.filter(responsable=user))

	return {k: list(v) for k, v in data.items()}

@login_required
def index(request):
	return render(request, "workload/accueil.html")