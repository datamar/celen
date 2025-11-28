from django.db import models
from django.urls import reverse
from ressource.models.utility import Cachet
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils.timezone import now
#from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

#########
# Mixin #
#########
class TimeBoundMixin(models.Model):
	"""
	Mixin générique pour les objets disposant de :
	- dates prévues (planned)
	- dates réelles (actual)
	"""
	start_date_prevue = models.DateField("Date prévue de début", null=True, blank=True)
	end_date_prevue = models.DateField("Date prévue de fin", null=True, blank=True)

	start_date_reel = models.DateField("Date réelle de début", null=True, blank=True)
	end_date_reel = models.DateField("Date réelle de fin", null=True, blank=True)

	class Meta:
		abstract = True

	@property
	def duree_prevue(self):
		"""Durée planifiée en jours (ou None)."""
		if self.start_date_prevue and self.end_date_prevue:
			return (self.end_date_prevue - self.start_date_prevue).days
		return None

	@property
	def duree_reelle(self):
		"""Durée réelle en jours (ou None)."""
		if self.start_date_reel and self.end_date_reel:
			return (self.end_date_reel - self.start_date_reel).days
		return None

	@property
	def is_started(self):
		return self.start_date_reel is not None

	@property
	def is_finished(self):
		return self.end_date_reel is not None

######################
# Classes abstraites #
######################
class BaseApp(Cachet):
	"""Projet, Mission, Livrable et Tâche hérite de ce truc."""
	nom = models.CharField(max_length=124, verbose_name="Nom")
	description = models.TextField(blank=True, verbose_name="Description")
	documents = models.ManyToManyField(
		"workload.Document", 
		blank=True, 
		help_text='Liens vers la GED',
		related_name="%(class)s_documents"
	)
	commentaires = GenericRelation(
		"Commentaire", 
		related_query_name="%(class)s"
	)
	implications = GenericRelation(
		"Implication", 
		related_query_name="%(class)s"
	)
	tags = TaggableManager(blank=True)

	def __str__(self):
		return self.nom

	class Meta:
		abstract = True

	def get_content_type_id(self):
		"""Retourne l'ID du ContentType pour cet objet"""
		return ContentType.objects.get_for_model(self.__class__).id

	def get_add_document_url(self):
		"""Retourne l'URL pour ajouter un document à cet objet"""
		return reverse('workload:document_create', kwargs={
			'content_type_id': self.get_content_type_id(),
			'object_id': self.pk
		})

######################
# Classes génériques #
######################
class Commentaire(Cachet):
	'''Commentaire générique pour tous les objets'''
	class Type(models.TextChoices):
		INFO = "INFO", "Information"
		BLOCAGE = "BLOCAGE", "Blocage"
		DECISION = "DECISION", "Décision"
		ACTION = "ACTION", "Action requise"

	type = models.CharField(max_length=8, choices=Type.choices, default=Type.INFO)
	contenu = models.TextField()

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	cible = GenericForeignKey("content_type", "object_id")

	class Meta:
		ordering = ["-created"]

	def __str__(self):
		return self.get_type_display()+" par "+self.created_by.username

class Implication(Cachet, TimeBoundMixin):
	"""Implication d'un Agent dans un Projet, Mission, Tâche ou Livrable"""
	class Nature(models.IntegerChoices):
		PONCTUELLE = 1, "Ponctuelle"
		RECURRENTE = 2, "Récurrente"
		CONTINUE = 3, "Continue"

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	cible = GenericForeignKey("content_type", "object_id")

	agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="implications")
	nature = models.IntegerField(choices=Nature.choices, default=Nature.CONTINUE)
	contribution = models.PositiveSmallIntegerField(
		default=0, 
		validators=[MinValueValidator(0), MaxValueValidator(100)],
	)
	role = models.CharField(max_length=124, blank=True, verbose_name="Rôle")

	def __str__(self):
		return f"{self.agent} - {self.role} dans {self.cible}"

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['content_type', 'object_id', "agent"], name="implication_unique")
		]

#####################
# Classes concrètes #
#####################
class Document(Cachet):
	'''Représente un lien vers la GED'''
	nom = models.CharField(max_length=124, blank=True, null=True)
	url = models.URLField()

	def save(self, *args, **kwargs):
		if not self.nom:
			self.nom = self.url.split("/")[-1]
		super().save(*args, **kwargs)

	def __str__(self):
		return self.nom

class Mission(BaseApp):
	'''Objet représentant les missions de la CELEN'''

	def get_absolute_url(self):
		return reverse("workload:mission_details", kwargs={"pk": self.pk})

class Projet(BaseApp, TimeBoundMixin):
	"""Un Projet est une activité planifiée menée dans le cadre d'une Mission"""
	class Status(models.TextChoices):
		DRAFT = "DRAFT", "Brouillon"
		PLANNED = "PLANNED", "Planifié"
		ACTIVE = "ACTIVE", "En cours"
		ON_HOLD = "ON_HOLD", "En pause"
		DONE = "DONE", "Terminé"
		CANCELED = "CANCELED", "Annulé"

		@classmethod
		def get_color(cls, status_code):
			color_map = {
				"DRAFT": "bg-secondary",
				"PLANNED": "bg-info",
				"ACTIVE": "bg-primary",
				"ON_HOLD": "bg-warning",
				"DONE": "bg-success",
				"CANCELED": "bg-dark",
			}
			return color_map.get(status_code, "bg-light")

	class Priority(models.IntegerChoices):
		LOW = 1, "Basse"
		MEDIUM = 2, "Moyenne"
		HIGH = 3, "Haute"

	mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="projets")
	r1 = models.ForeignKey(User, verbose_name="Coordinateur", help_text="Responsable du projet", on_delete=models.SET_NULL, related_name="projets_coordonnes", null=True, blank=True)
	r2 = models.ForeignKey(User, verbose_name="BackUp", help_text="Remplaçant du coordinateur", on_delete=models.SET_NULL, related_name="projets_backup", null=True, blank=True)
	status = models.CharField(max_length=16, choices=Status.choices, default=Status.PLANNED)
	priorite = models.IntegerField(choices=Priority.choices, default=Priority.MEDIUM)
	percent_complete = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Progression (%)")

	def get_status_color(self):
		return self.Status.get_color(self.status)

	def get_priority_class(self):
		return {
			1: "success",
			2: "warning",
			3: "danger",
		}.get(self.priorite, "light")
	
	def get_absolute_url(self):
		return reverse("workload:projet_details", kwargs={"pk": self.pk})

	def _get_progression_livrable(self, livrable):
		"""Convertit le statut du livrable en pourcentage"""
		progression_map = {
			Livrable.Status.PLANNED: 0,
			Livrable.Status.DUE: 25,
			Livrable.Status.SUBMITTED: 75,
			Livrable.Status.APPROVED: 100,
			Livrable.Status.REJECTED: 0,
		}
		return progression_map.get(livrable.status, 0)

	@property
	def est_en_retard(self):
		if self.status in [self.Status.DONE, self.Status.CANCELED]:
			return False
		return super().est_en_retard

	@classmethod
	def get_statuts(cls):
		queryset = (
			cls.objects
			.values("status")
			.annotate(count=models.Count("status"))
			.order_by()
		)
		return [
			{
				"code": item["status"],
				"label": cls.Status(item["status"]).label,
				"count": item["count"],
				"color": cls.Status.get_color(item["status"]),
			}
			for item in queryset
		]

class Livrable(BaseApp, TimeBoundMixin):
	class Status(models.TextChoices):
		PLANNED = "PLANNED", "Planifié"
		DUE = "DUE", "Échu"
		SUBMITTED = "SUBMITTED", "Soumis"
		APPROVED = "APPROVED", "Validé"
		REJECTED = "REJECTED", "Rejeté"

	projet = models.ForeignKey(
		Projet, 
		on_delete=models.CASCADE, 
		related_name="livrables",
		verbose_name="Projet parent"
	)
	responsable = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		related_name="livrables_responsable",
		verbose_name="Responsable du livrable",
		null=True,
		blank=True
	)

	status = models.CharField(max_length=16, choices=Status.choices, default=Status.PLANNED)
	depends_on = models.ForeignKey(
		"self", 
		on_delete=models.SET_NULL, 
		null=True, 
		blank=True, 
		related_name="livrables_dependants",
		verbose_name="Dépend de"
	)

	def __str__(self):
		return f"{self.nom} ({self.projet})"

	def get_absolute_url(self):
		return reverse("workload:livrable_details", kwargs={"pk": self.pk})

	def clean(self):
		super().clean() # sans ça, cette méthode "clean" écrase celle du Mixin
		if self.depends_on and self.depends_on == self:
			raise ValidationError("Un livrable ne peut dépendre de lui-même.")

	class Meta:
		ordering = ['end_date_prevue']

class Tache(BaseApp):
	"""Une Tâche s'effectue dans le cadre d'un Projet ou d'une Mission. Une Tâche n'a pas de date de début ni de fin et n'est pas lié, ni n'a d'attribut de progression. Elle est finie ou non. Une Tache ne peut être attribué qu'à un seul Agent"""
	complete = models.BooleanField(default=False, verbose_name="La tâche est-elle terminée ?")
	mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="taches", null=True, blank=True)
	projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name="taches", null=True, blank=True)

	def get_absolute_url(self):
		return reverse("workload:tache_details", kwargs={"pk": self.pk})