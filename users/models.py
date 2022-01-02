from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserActivity(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    last_visit = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username.username


@receiver(post_save, sender=User)
def create_user_activity(sender, instance, created, **kwargs):
    if created:
        UserActivity.objects.create(username=instance)


@receiver(post_save, sender=User)
def save_user_activity(sender, instance, **kwargs):
    instance.useractivity.save()

