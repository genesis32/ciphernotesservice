from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return "%s" % (self.name)

class User(models.Model):
    email   = models.EmailField()
    name    = models.CharField(max_length=256)
    pin     = models.CharField(max_length=256)
    sysid   = models.CharField(max_length=64, unique=True)
    pubkey  = models.CharField(max_length=1024, null=True)
    enabled = models.BooleanField(default="False")
    organization = models.ForeignKey(Organization)
    num_failures = models.IntegerField()
    activated = models.BooleanField(default="False")

    def __unicode__(self):
        return "%s" % (self.email)

