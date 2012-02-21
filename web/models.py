from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from core.models import Organization

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    organization = models.ForeignKey(Organization, null=True)
    accepted_eula = models.BooleanField()

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
