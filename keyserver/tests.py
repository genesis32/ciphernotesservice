import json
import urllib
from django.test import TestCase
from django.test.client import Client

from models import *
from statuscodes import StatusCodes

class TestViews(TestCase):
    def setUp(self):
        pass

    def _encformdata(self, params):
       return urllib.urlencode(params) 

    def test_activated(self):
        c = Client()
        response = c.get('/keyserver/device/activated/E03B689E-7E06-5F39-A7DC-8F0E103C3325')
        resp = json.loads(response.content)
        self.assertEquals(resp['resultcode'], StatusCodes.DeviceIsNotActivated)

    def test_doesnotexist(self):
        c = Client()
        response = c.get('/keyserver/device/activated/A03B689E-7E06-5F39-A7DC-8F0E103C3325')
        resp = json.loads(response.content)
        self.assertEquals(resp['resultcode'], StatusCodes.DeviceNotFound)

    def test_activate(self):
        c = Client()
        fdata = self._encformdata({'pubkey': '--RSA+PUBKEY--'})
        response = c.post('/keyserver/device/activate/E03B689E-7E06-5F39-A7DC-8F0E103C3325', fdata, content_type='application/x-www-form-urlencoded')
        resp = json.loads(response.content)
        self.assertEquals(StatusCodes.DeviceNowActivated, resp['resultcode'])
        
        d = Device.objects.get(udid='E03B689E-7E06-5F39-A7DC-8F0E103C3325')
        self.assertEquals('--RSA+PUBKEY--', d.owner.pubkey) 

    def test_getpubkey(self):
        c = Client()
        response = c.get('/keyserver/pubkey/get/1')
        resp = json.loads(response.content)
        assert(resp['pubkey'] != None)

    def test_pubmessage(self):
        c = Client()
        fdata = self._encformdata({ 'frid': 1, 'toid': 2, 'msg': 'enc message' })
        response = c.post('/keyserver/message/send', fdata, content_type='application/x-www-form-urlencoded')
        resp = json.loads(response.content)
        self.assertEquals(StatusCodes.MessageSent, resp['resultcode'])

    def test_getmessage(self):
        c = Client()
        fdata = self._encformdata({ 'frid': 1, 'toid': 2, 'msg': 'enc message' })
        response = c.post('/keyserver/message/send', fdata, content_type='application/x-www-form-urlencoded')
        resp = json.loads(response.content)
        self.assertEquals(StatusCodes.MessageSent, resp['resultcode'])

        response = c.get('/keyserver/message/get/1')
        resp = json.loads(response.content)
        self.assertEquals(StatusCodes.MessageFound, resp['resultcode'])

    def test_pubenckey(self):
        c = Client()
        fdata = self._encformdata({ 'frid': 1, 'toid': 2, 'msg': 'enc message' })
        response = c.post('/keyserver/message/send', fdata, content_type='application/x-www-form-urlencoded')

        resp = json.loads(response.content)
        self.assertEquals(StatusCodes.MessageSent, resp['resultcode'])

        response = c.post('/keyserver/msgkey/send', { 'msgid': 1, 'key': 'abcdef' })
        resp = json.loads(response.content)
        self.assertEquals(StatusCodes.KeySent, resp['resultcode'])

    def test_listcontacts(self):
        c = Client()
        response = c.get('/keyserver/contacts/get/E03B689E-7E06-5F39-A7DC-8F0E103C3325')
        resp = json.loads(response.content)
        self.assertEquals(2, len(resp['contacts']))
        
    def test_pubmessage_failedfr(self):
        c = Client()
        fdata = self._encformdata({ 'frid': 4, 'toid': 2, 'msg': 'enc message' })
        response = c.post('/keyserver/message/send', fdata, content_type='application/x-www-form-urlencoded')
        resp = json.loads(response.content)
        self.assertEquals(StatusCodes.MessageSendFailedInvalidUser, resp['resultcode'])

    def test_pubmessage_failedto(self):
        c = Client()
        fdata = self._encformdata({ 'frid': 1, 'toid': 4, 'msg': 'enc message' })
        response = c.post('/keyserver/message/send', fdata, content_type='application/x-www-form-urlencoded')
        resp = json.loads(response.content)
        self.assertEquals(StatusCodes.MessageSendFailedInvalidUser, resp['resultcode'])

    def test_pubmessage_failedboth(self):
        c = Client()
        fdata = self._encformdata({ 'frid': 4, 'toid': 3, 'msg': 'enc message' })
        response = c.post('/keyserver/message/send', fdata, content_type='application/x-www-form-urlencoded')
        resp = json.loads(response.content)
        self.assertEquals(StatusCodes.MessageSendFailedInvalidUser, resp['resultcode'])
    
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
