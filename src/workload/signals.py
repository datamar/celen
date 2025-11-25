# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from workload.models import Projet, Livrable, Implication
from django.contrib.contenttypes.models import ContentType

def ajouter_implication(agent, cible, role):
    if agent is None:
        return

    content_type = ContentType.objects.get_for_model(cible)
    # Vérifie si une implication existe déjà
    if not Implication.objects.filter(
        content_type=content_type,
        object_id=cible.id,
        agent=agent
    ).exists():
        Implication.objects.create(
            content_type=content_type,
            object_id=cible.id,
            agent=agent,
            role=role,
            contribution=0
        )

@receiver(post_save, sender=Projet)
def projet_add_responsables_as_implications(sender, instance, **kwargs):
    ajouter_implication(instance.r1, instance, "Responsable")
    if instance.r2:
        ajouter_implication(instance.r2, instance, "Backup")

@receiver(post_save, sender=Livrable)
def livrable_add_responsable_as_implication(sender, instance, **kwargs):
    ajouter_implication(instance.responsable, instance, "Responsable du livrable")
