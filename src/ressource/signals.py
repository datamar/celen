from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from ressource.models.users import Profil
from crum import get_current_user

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        requesting_user = get_current_user()
        profil = Profil.objects.create(user=instance, created_by=requesting_user)
        if instance.is_superuser:
            admin_group = Group.objects.get(name='Superadmin')
            instance.groups.add(admin_group)
        profil.save()
