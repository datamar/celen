from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta
from crum import get_current_user
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Cachet(models.Model):
    """
    Classe abstraite pour tracer l’auteur et la date de création/modification.
    """
    created = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(
        User, blank=True, null=True, editable=False,
        on_delete=models.SET_NULL, default=None,
        related_name='%(app_label)s_%(class)s_created'
    )
    modified = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.ForeignKey(
        User, editable=False, blank=True, null=True,
        on_delete=models.SET_NULL, default=None,
        related_name='%(app_label)s_%(class)s_modified'
    )

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and user.is_authenticated:
            if not self.pk:
                self.created_by = user
            else:
                self.modified_by = user
        super().save(*args, **kwargs)

    @property
    def is_modified(self):
        return (self.modified - self.created) > timedelta(seconds=1)

    class Meta:
        abstract = True
