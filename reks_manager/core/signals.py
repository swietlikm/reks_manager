# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from .models import Animal, HealthCard
#
#
# @receiver(post_save, sender=Animal)
# def create_health_card(sender, instance, created, **kwargs):
#     if created:
#         HealthCard.objects.create(animal=instance)
#
