from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from workload.models import *
from django.db.models import Q
from datetime import timedelta, date

def get_calendar_events():
    events = []

    for model in (Projet, Livrable, Implication):
        for obj in model.objects.all():
            for label, date in obj.get_all_dates().items():
                if date:
                    events.append({
                        "id": obj.id,
                        "label": label,
                        "date": date,  # important pour JS
                        "type": obj.__class__.__name__.lower(),
						"instance":obj
                    })

    return events


def get_objects_this_month():
	today = date.today()
	first_day = today.replace(day=1)
	next_month = today.replace(month=today.month % 12 + 1, day=1)
	last_day = next_month - timedelta(days=1)

	# Condition Q commune
	date_filter = (
		Q(start_date_prevue__range=(first_day, last_day)) |
		Q(end_date_prevue__range=(first_day, last_day)) |
		Q(start_date_reel__range=(first_day, last_day)) |
		Q(end_date_reel__range=(first_day, last_day))
	)

	projets = Projet.objects.filter(date_filter)

	livrables = Livrable.objects.filter(date_filter)

	implications = Implication.objects.filter(date_filter)

	return {
		"projets": projets,
		"livrables": livrables,
		"implications": implications,
	}

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
	mon_activite = get_objects_grouped(request.user)
	ce_mois_ci = get_objects_this_month()
	calendar_events = get_calendar_events()
	return render(request, "workload/accueil.html",{
		"users":User.objects.all(),
		"missions":Mission.objects.all(),
		"documents":Document.objects.all(),
		"projets":Projet.objects.all(),
		"commentaires":Commentaire.objects.all(),
		"taches":Tache.objects.all(),
		"livrables":Livrable.objects.all(),
		"mon_activite":mon_activite,
		"ce_mois_ci":ce_mois_ci,
		#"calendar_events":calendar_events,
		})


 