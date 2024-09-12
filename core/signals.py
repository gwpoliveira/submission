from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from core.models import Profile

@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            # Tenta criar o perfil apenas se não existir
            Profile.objects.create(user=instance)
        except Profile.DoesNotExist:
            # Se o perfil já existir, não tenta recriá-lo
            print(f"Perfil já existe para o usuário {instance.username}")
