from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from generales.models import Posgrado

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Hombre'),
        ('F', 'Mujer'),
    )
    gender = models.CharField(_('género'), max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    apellido_materno = models.CharField(_('apellido materno'), max_length=150, blank=True, null=True)
    posgrado = models.ManyToManyField(Posgrado, blank=True, verbose_name=_("Posgrado"))  # Cambiado a ManyToManyField
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between and includes the apellido_materno if it exists.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        if self.apellido_materno:
            full_name += ' %s' % self.apellido_materno
        return full_name.strip()
