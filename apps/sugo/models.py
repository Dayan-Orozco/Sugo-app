from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from apps.user.models import *

# Modelo para los diferentes tipos de cuenta (Binance, Nequi, etc.)
class AccountType(models.Model):
    name = models.CharField("Nombre del tipo de cuenta", max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tipo de Cuenta"
        verbose_name_plural = "Tipos de Cuenta"
        ordering = ["-name"]

# Modelo que representa a cada streamer o chica
class Streamer(models.Model):
    STATUS_CHOICES = [
        ('active', 'Activa'),
        ('inactive', 'Inactiva'),
        ('new', 'Nueva'),
        ('intermediate', 'Intermedia'),
        ('newbie', 'Novata'),
        ('resting', 'Descanso'),
        ('no_income_7', '7 días sin generar'),
        ('no_income_15', '15 días sin generar'),
        ('no_income_30', '30 días sin generar'),
        ('waiting_sugo', 'Esperando aprobación'),
        ('my_agency_btn', 'Botón Mi Agencia'),
        ('duplicate', 'Duplicado'),
        ('released', 'Liberada'),
    ]
    COUNTRY_CHOICES = [
        ('col', 'Colombia'),
        ('ven', 'Venezuela'),
        ('mex', 'Mexico'),
        ('bol', 'Bolivia'),
        ('per', 'Perú'),
        ('arg', 'Argentina'),
        ('ecu', 'Ecuador'),
        ('crc', 'Costa Rica'),
    ]
    CHARM_LEVEL_CHOICES = [
        (0, 'Nivel 0 – Nueva'),
        (1, 'Nivel 1 – Principiante +5,000 diamantes'),
        (2, 'Nivel 2 – Intermedia +25,000 diamantes'),
        (3, 'Nivel 3 – Activa +100,000 diamantes'),
        (4, 'Nivel 4 – Activa +450,000 diamantes'),
        (5, 'Nivel 5 – Activa +2,045,000 diamantes'),
    ]
    VIP_LEVEL_CHOICES = [
        ("0", 'VIP 0'),
        ("1", 'VIP 1'),
        ("2", 'VIP 2'),
        ("3", 'VIP 3'),
        ("4", 'VIP 4'),
        ("5", 'VIP 5'),
        ("6", 'VIP 6'),
        ("7", 'VIP 7'),
        ("8", 'VIP 8'),
    ]
    id = models.IntegerField(primary_key=True, unique=True, verbose_name="ID SUGO")
    name = models.CharField("Apodo", max_length=150)
    real_name = models.CharField("Nombre real", max_length=150, blank=True, null=True)
    profile_picture = models.ImageField("Foto de perfil", upload_to='streamers/profile_pics/', blank=True, null=True)
    telegram_number = models.CharField("Número de Telegram", max_length=20, blank=True, null=True)
    whatsapp_number = models.CharField("Número de WhatsApp", max_length=20, blank=True, null=True)
    join_date = models.DateTimeField("Fecha de ingreso", blank=True, null=True)
    country = models.CharField("País", max_length=15,  choices=COUNTRY_CHOICES)
    vip_level = models.CharField("Nivel VIP", max_length=10, choices=VIP_LEVEL_CHOICES)
    status = models.CharField("Estado", max_length=50, choices=STATUS_CHOICES, default='new')
    charm_level = models.IntegerField("Nivel de Encanto", choices=CHARM_LEVEL_CHOICES, default=0)
    account_type = models.ForeignKey(AccountType, on_delete=models.SET_NULL, null=True, verbose_name="Tipo de cuenta", blank=True)
    account_details = models.CharField("Cuenta para recibir dinero", max_length=255, blank=True, null=True)
    qr_binance_picture = models.ImageField("QR de Binance", upload_to='streamers/qr_binance/', blank=True, null=True)
    binance_id = models.BigIntegerField("ID de Binance", blank=True, null=True)
    is_capacite = models.BooleanField("¿Ya Fue Capacitada?", default=False)
    date_capacite = models.DateTimeField("Fecha de Capacitación", blank=True, null=True)
    reuse_acount = models.CharField("Cuenta Reuzada", max_length=255, blank=True, null=True)  
    enable = models.BooleanField("Habilitado/Inhabilitado", default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Usuario Asociado", blank=True)

    def __str__(self):
        return f"{self.name} ({self.id})"

    class Meta:
        verbose_name = "Streamer"
        verbose_name_plural = "Streamers"
        ordering = ["-join_date"]

# Modelo que representa un grupo de retiros (como un lote)
class WithdrawalGroup(models.Model):
    name = models.CharField("Nombre del grupo", max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Grupo de Retiro"
        verbose_name_plural = "Grupos de Retiro"
        ordering = ["-created_at"]

# Modelo que representa un retiro individual de una streamer
class Withdrawal(models.Model):
    streamer = models.ForeignKey('Streamer', verbose_name="Streamer", on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(WithdrawalGroup, verbose_name="Grupo de retiro", on_delete=models.SET_NULL, related_name="withdrawals", null=True)
    amount_usd = models.DecimalField("Monto en USD", max_digits=10, decimal_places=2)
    withdrawal_date = models.DateField("Fecha del retiro")

    def __str__(self):
        return f"{self.streamer.real_name} - ${self.amount_usd} ({self.withdrawal_date})"

    class Meta:
        verbose_name = "Retiro"
        verbose_name_plural = "Retiros"
        ordering = ["-withdrawal_date"]

# Modelo para los niveles de la agencia con su porcentaje de comisión
class AgencyLevel(models.Model):
    LEVEL_CHOICES = [
        ('n', 'N – Comisión 10%'),
        ('d', 'D – Comisión 14%'),
        ('c', 'C – Comisión 18%'),
        ('b', 'B – Comisión 22%'),
        ('a', 'A – Comisión 26%'),
        ('s', 'S – Comisión 30%'),
    ]
    level = models.CharField("Nivel de agencia", choices=LEVEL_CHOICES, max_length=1, default='n')
    name = models.CharField("Nombre del grupo", max_length=100, unique=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"

    class Meta:
        verbose_name = "Nivel de Agencia"
        verbose_name_plural = "Niveles de Agencia"
        ordering = ["name"]

# Modelo que registra el rendimiento diario de cada chica
class DailyPerformance(models.Model):
    date = models.DateField("Fecha", default=timezone.now)
    streamer = models.ForeignKey('Streamer', verbose_name="Streamer", on_delete=models.SET_NULL, null=True)
    streamer_name = models.CharField("Nombre de la Streamer", max_length=150)
    total_diamonds = models.PositiveIntegerField("Diamantes totales")
    diamonds_chat = models.PositiveIntegerField("Diamantes por chat")
    diamonds_gifts = models.PositiveIntegerField("Diamantes por regalitos")
    diamonds_video = models.PositiveIntegerField("Diamantes por videollamadas")

    def __str__(self):
        return f"{self.streamer_name} - {self.date} - {self.total_diamonds} diamantes"

    class Meta:
        verbose_name = "Rendimiento Diario"
        verbose_name_plural = "Rendimientos Diarios"
        ordering = ["-date"]
