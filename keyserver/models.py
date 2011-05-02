from django.db import models

class User(models.Model):
    email         = models.EmailField()
    activated     = models.BooleanField()
    activation_id = models.CharField(max_length=64)
    pubkey        = models.CharField(max_length=1024)
    ipad_udid     = models.CharField(max_length=64)

    def __str__(self):
        return "%s" % (self.email)
