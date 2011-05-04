from django.test import TestCase
from models import *

class TestUserFunctions(TestCase):
    def setUp(self):
        pass

    def test_CreateUser(self):
        u1 = User(email='***REMOVED***', pubkey='fillin')
        u1.save()

    def test_TwoUserAssoc(self):
        u1 = User(email='***REMOVED***', pubkey='fillin')
        u1.save()
        u2 = User(email='***REMOVED***', pubkey='fillin')
        u2.save()

        ua1 = UserAssociation(user1=u1, user2=u2, invitation_code=4832, invitation_accepted=True)
        ua1.save()

        assert(ua1.user1 == u1 and ua1.user2 == u2 and ua1.invitation_code == 4832)
        
class TestMessageSend(TestCase):
    def setUp(self):
        self.u1 = User(email='***REMOVED***', pubkey='fillin')
        self.u1.save()
        self.u2 = User(email='***REMOVED***', pubkey='fillin')
        self.u2.save()
    
    def test_MessageSend(self):
       m1 = Message(from_user = self.u1, to_user = self.u2, enc_msg='<ciphertest>')
       m1.save()
       key = Key(message=m1, key='deadbeef', expires='2012-10-10') 
       key.save()
