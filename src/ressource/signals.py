from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from ressource.models.users import Profil
from django.contrib.auth import get_user_model
from crum import get_current_user
from django.core.mail import send_mail
from django.conf import settings
#from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        requesting_user = get_current_user()
        profil = Profil.objects.create(user=instance, created_by=requesting_user)
        # Sauvegarder le profil
        profil.save()
    # Ajouter au groupe Superadmin si applicable
    if instance.is_superuser:
        try:
            admin_group = Group.objects.get(name='Superadmin')
            instance.groups.add(admin_group)
        except Group.DoesNotExist:
            pass

    # --- ENVOI EMAIL DE CONFIRMATION (allauth 65.12.0) ---
    if instance.email:
        email_obj, _ = EmailAddress.objects.get_or_create(
            user=instance,
            email=instance.email.lower(),
            defaults={
                "verified": False,
                "primary": True
            }
        )

        # 👇 Appel officiel
        email_obj.send_confirmation(
            request=None,   # pas de request dans un signal
            signup=False    # user créé hors signup allauth
        )