from django.db import models

class User(models.Model):
    email   = models.EmailField()
    pubkey  = models.CharField(max_length=1024)

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
    from_user = models.ForeignKey(User, related_name='from_user')
    to_user   = models.ForeignKey(User, related_name='to_user')
    enc_msg   = models.TextField()

class Key(models.Model):
    message = models.ForeignKey(Message)
    key     = models.CharField(max_length=256)
    expires = models.DateField(null=True)
    
    def __unicode__(self):
        return "key: %s - expires: %s" % (self.key, self.expires)

class Device(models.Model):
    owner     = models.ForeignKey(User)
    udid      = models.CharField(max_length=128)
    activated = models.BooleanField()
    pin       = models.IntegerField()

    def __unicode__(self):
        return "Device: %s UDID:%s" % (self.owner.email, self.udid)

