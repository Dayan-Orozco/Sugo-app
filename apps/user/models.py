from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class User(AbstractUser):
    COUNTRY_PREFIXES = {
        'arg': '+54',   # Argentina
        'bol': '+591',  # Bolivia
        'chl': '+56',   # Chile
        'col': '+57',   # Colombia
        'crc': '+506',  # Costa Rica
        'dom': '+1-809',# República Dominicana (también +1-829, +1-849)
        'ecu': '+593',  # Ecuador
        'slv': '+503',  # El Salvador
        'gtm': '+502',  # Guatemala
        'hnd': '+504',  # Honduras
        'mex': '+52',   # México
        'nic': '+505',  # Nicaragua
        'pan': '+507',  # Panamá
        'par': '+595',  # Paraguay
        'per': '+51',   # Perú
        'pry': '+1-787',# Puerto Rico (también +1-939)
        'uru': '+598',  # Uruguay
        'ven': '+58',   # Venezuela
    }
    COUNTRY_CHOICES = [
        ('arg', '🇦🇷 - Argentina'),
        ('bol', '🇧🇴 - Bolivia'),
        ('chl', '🇨🇱 - Chile'),
        ('col', '🇨🇴 - Colombia'),
        ('crc', '🇨🇷 - Costa Rica'),
        ('dom', '🇩🇴 - República Dominicana'),
        ('ecu', '🇪🇨 - Ecuador'),
        ('slv', '🇸🇻 - El Salvador'),
        ('gtm', '🇬🇹 - Guatemala'),
        ('hnd', '🇭🇳 - Honduras'),
        ('mex', '🇲🇽 - México'),
        ('nic', '🇳🇮 - Nicaragua'),
        ('pan', '🇵🇦 - Panamá'),
        ('par', '🇵🇾 - Paraguay'),
        ('per', '🇵🇪 - Perú'),
        ('pry', '🇵🇷 - Puerto Rico'),
        ('uru', '🇺🇾 - Uruguay'),
        ('ven', '🇻🇪 - Venezuela'),
    ]

    country = models.CharField("País", max_length=15, choices=COUNTRY_CHOICES, default="col")
    document = models.BigIntegerField("Documento / Identificacion", default=None)
    telegram_number = models.CharField("Número o Usuario de Telegram", max_length=20, blank=True, null=True)
    phone = models.CharField("Número de Telefono", max_length=10, blank=False, null=False, unique=True)
    EMAIL_FIELD = None 

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['country', 'document'], name='unique_document_per_country')
        ]
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Si no tiene grupo, asignar por defecto al grupo "Streamer"
        if not self.groups.exists():
            grupo, _ = Group.objects.get_or_create(name='Streamers')
            self.groups.add(grupo)

        # Agregar prefijo de país al número de Telegram si existe
        if self.telegram_number:
            if not self.telegram_number.startswith('@'):
                if self.country in User.COUNTRY_PREFIXES:
                    prefix = User.COUNTRY_PREFIXES[self.country]
                    if not self.telegram_number.startswith(prefix):
                        self.telegram_number = f"{prefix}{self.telegram_number}"
                        print("telegram_number t.me/", self.telegram_number)
                        super().save(update_fields=["telegram_number"])
