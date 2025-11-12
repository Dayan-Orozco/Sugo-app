from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import *

@receiver(pre_save, sender=WithdrawalGroup)
def set_nombre_retiro_group(sender, instance, **kwargs):
    if not instance.nombre:
        fecha_actual = timezone.now().date().isoformat()  # ejemplo: '2025-08-05'
        instance.nombre = f"Retiro-{fecha_actual}"

@receiver(pre_save, sender=Streamer)
def presave_streamers(sender, instance, **kwargs):
    # CORRECCION DE NUMEROS
    if instance.telegram_number:
        instance.telegram_number = str(instance.telegram_number).replace(' ', '').strip() if instance.telegram_number else ''
    if instance.whatsapp_number:
        instance.whatsapp_number = str(instance.whatsapp_number).replace(' ', '').strip() if instance.whatsapp_number else ''
    
    # SE ASIGNA NOMBRE EN CASO DE VENIR VACIO
    # print("Nombre real", instance.real_name, " - ",instance.name, instance.join_date)
    if not instance.real_name:
        if instance.real_name is None:
            # print("Entra y actualiza nombre") 
            instance.real_name = instance.name
    
    # SE VALIDA Y ASIGNAN ESTADOS
    status_before = None
    if instance.id: 
        status_before = Streamer.objects.get(id=instance.id).status

    print("Se ejcuta el Presave de Streamers", instance.charm_level, instance, instance.vip_level, "Estado anterior", status_before, "estado nuevo", instance.status )
    if status_before == "new" or status_before == "newbie" or status_before == "intermediate" or status_before == "active" or status_before == "inactive" or status_before == "resting" or status_before == "no_income_7" or status_before == "no_income_15" or status_before == "no_income_30" and instance.status == "waiting_sugo" or instance.status == "my_agency_btn" or instance.status == "duplicate":  
        print("Quita la fecha")
        instance.join_date = None

    # print("Nombre real", instance.real_name, " - ",instance.name, instance.join_date)
    if not instance.real_name:
        if instance.real_name is None:
            # print("Entra y actualiza nombre") 
            instance.real_name = instance.name
    if instance.join_date:
        if instance.charm_level == 0:
            # print("Es principiante")
            instance.status = "new"
        elif instance.charm_level == 1:
            # print("Es Nueva")
            instance.status = "newbie"
        elif instance.charm_level == 2:
            # print("Es intermedia")
            instance.status = "intermediate"
        elif instance.charm_level >= 3:
            # print("Es activa")
            instance.status = "active"