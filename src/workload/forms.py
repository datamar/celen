from django import forms
from workload.models import Implication, Document, Commentaire, Projet, Tache, Livrable
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ImplicationForm(forms.ModelForm):
    class Meta:
        model = Implication
        fields = [
            "agent",
            "nature",
            "contribution",
            "role",
            "start_date_prevue",
            "end_date_prevue",
            "start_date_reel",
            "end_date_reel",
        ]
        widgets = {
            "start_date_prevue": forms.DateInput(attrs={"type": "date"}),
            "end_date_prevue": forms.DateInput(attrs={"type": "date"}),
            "start_date_reel": forms.DateInput(attrs={"type": "date"}),
            "end_date_reel": forms.DateInput(attrs={"type": "date"}),
            "contribution": forms.NumberInput(attrs={
                "type": "range", 
                "min": 0, 
                "max": 100, 
                "class": "form-range"}),

        }

    def clean(self):
        cleaned_data = super().clean()
        agent = cleaned_data.get("agent")

        if not self.instance.pk:  # seulement à la création
            content_type = self.initial.get("content_type")
            object_id = self.initial.get("object_id")

            # vérification de la contrainte d’unicité
            if Implication.objects.filter(
                content_type_id=content_type,
                object_id=object_id,
                agent=agent
            ).exists():
                raise ValidationError("Cet agent est déjà impliqué dans cet objet.")

        return cleaned_data

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ["type", "contenu"]

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['nom', 'url']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Si vide, sera remplacé par l'identifiant de l'url"
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lien complet vers la GED',
                'required': True
            }),
        }

class ProjetForm(forms.ModelForm):
    class Meta:
        model = Projet
        exclude = ("documents", "commentaires","implications")
        widgets = {
            "start_date_prevue": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "end_date_prevue": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "start_date_reel": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "end_date_reel": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "percent_complete": forms.NumberInput(attrs={
                "type": "range", 
                "min": 0, 
                "max": 100, 
                "class": "form-range"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sans ça, Django n’affiche pas la date existante
        for field in [
            "start_date_prevue",
            "end_date_prevue",
            "start_date_reel",
            "end_date_reel",
        ]:
            if self.instance and getattr(self.instance, field):
                # Force le format HTML5
                self.fields[field].initial = getattr(self.instance, field).strftime("%Y-%m-%d")
        
class TacheForm(forms.ModelForm):
    class Meta:
        model = Tache
        fields = [
            "nom",
            "description",
            "complete",
            "mission",
            "projet",
            "tags",
        ]

class LivrableForm(forms.ModelForm):
    class Meta:
        model = Livrable
        fields = "__all__"
        widgets = {
            "start_date_prevue": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "end_date_prevue": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "start_date_reel": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "end_date_reel": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sans ça, Django n’affiche pas la date existante
        for field in [
            "start_date_prevue",
            "end_date_prevue",
            "start_date_reel",
            "end_date_reel",
        ]:
            if self.instance and getattr(self.instance, field):
                # Force le format HTML5
                self.fields[field].initial = getattr(self.instance, field).strftime("%Y-%m-%d")