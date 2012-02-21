from django.db import models

from core.models import User

class UserSession(models.Model):
    user = models.ForeignKey(User)
    session_id = models.CharField(max_length=256)
    last_update = models.DateTimeField(auto_now=True)

