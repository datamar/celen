from django.contrib import admin
from workload.models import Mission, Projet, Livrable, Tache, Implication

admin.site.register([Mission, Projet, Livrable, Tache, Implication])