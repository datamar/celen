import os
from django.db import models
from PIL import Image
from django.contrib.auth import get_user_model
from ressource.models.utility import Cachet
from allauth.account.models import EmailAddress
from django.utils.translation import gettext_lazy as _
from workload.models import Implication

User = get_user_model()

class Profil(Cachet):
    def profile_image_upload_to(instance, filename):
        user_folder = f'{instance.user.username}/avatar/'
        return os.path.join(user_folder, filename)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.CharField(max_length=255, blank=True, null=True, help_text=_("Quelques mots pour vous décrire"))
    photo = models.ImageField(default='user_default.jpg', upload_to=profile_image_upload_to, verbose_name="Avatar")
    phone = models.CharField(max_length=25, blank=True, null=True)

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)

    def __str__(self):
        if self.user.last_name and self.user.first_name:
            return self.user.get_full_name()
        else:
            return self.user.username

    @property
    # Emails
    def emails_secondaires(self):
        return EmailAddress.objects.filter(user=self.user).exclude(primary=True)

    @property
    def total_contribution(self):
        return (
            Implication.objects
            .filter(agent=self.user)
            .aggregate(total=models.Sum("contribution"))["total"]
        ) or 0