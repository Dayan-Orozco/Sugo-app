from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class User(AbstractUser):
    COUNTRY_CHOICES = [
        ('col', '🇨🇴 - Colombia'),
        ('ven', '🇻🇪 - Venezuela'),
        ('mex', '🇲🇽 - México'),
        ('bol', '🇧🇴 - Bolivia'),
        ('per', '🇵🇪 - Perú'),
        ('arg', '🇦🇷 - Argentina'),
        ('ecu', '🇪🇨 - Ecuador'),
        ('crc', '🇨🇷 - Costa Rica'),
    ]
    country = models.CharField("País", max_length=15, choices=COUNTRY_CHOICES, default="col")
    document = models.IntegerField("Documento / Identificacion", default=None)
    telegram_number = models.CharField("Número de Telegram", max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Si no tiene grupo, asignar por defecto al grupo "Streamer"
        if not self.groups.exists():
            grupo, _ = Group.objects.get_or_create(name='Streamers')
            self.groups.add(grupo)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
