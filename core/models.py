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

class UserAssociation(models.Model):
    user1 = models.ForeignKey(User, related_name='user1')
    user2 = models.ForeignKey(User, related_name='user2')
    invitation_code = models.IntegerField()
    invitation_accepted = models.BooleanField(default="False")

    def __unicode__(self):
        return "%s - %s" % (self.user1, self.user2)

class Message(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', null=True, blank=True)
    from_org  = models.ForeignKey(Organization, related_name='from_org', null=True, blank=True)
    sysid     = models.CharField(max_length=64, unique=True)
    to_user   = models.ForeignKey(User, related_name='to_user')
    enc_msg   = models.TextField()
    
class Key(models.Model):
    message = models.ForeignKey(Message)
    sysid   = models.CharField(max_length=64, unique=True)
    key     = models.CharField(max_length=256)
    min_to_expire = models.IntegerField()
    expires = models.DateTimeField(null=True)
    
    def __unicode__(self):
        return "key: %s - expires: %s" % (self.key, self.expires)
