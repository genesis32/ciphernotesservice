import json
import urllib

from django.test import TestCase
from django.test.client import Client

from models import *

class TestViews(TestCase):
    def setUp(self):
        pass

    def _auth(self):
        c = Client()
        response = c.post('/keyserver/user/auth', {'email': '***REMOVED***', 'pin': '1234'}) 
        resp = json.loads(response.content)
        return resp['sessionid']

    def test_auth(self):
        c = Client()
        response = c.post('/keyserver/user/auth', {'email': '***REMOVED***', 'pin': '1234'}) 
        resp = json.loads(response.content)
        self.assertEquals(resp['success'], True)

    def test_badauth(self):
        c = Client()
        response = c.post('/keyserver/user/auth', {'email': '***REMOVED***', 'pin': '9234'})
        resp = json.loads(response.content)
        self.assertEquals(resp['success'], False)

    def test_2auth(self):
        c = Client()
        fdata = {'email': '***REMOVED***', 'pin': '1234'}
        response = c.post('/keyserver/user/auth', fdata)
        response = c.post('/keyserver/user/auth', fdata)
        resp = json.loads(response.content)
        self.assertEquals(resp['success'], True)

    def test_activated(self):
        c = Client()
        sessid = self._auth()
        pdata = {'sessionid': sessid}
        response = c.post('/keyserver/user/activated', pdata)
        resp = json.loads(response.content)
        self.assertEquals(resp['resultcode'], 1)

    def test_activate(self):
        c = Client()
        sessid = self._auth()
        pdata = {'sessionid': sessid, 'pubkey': '--RSA+PUBKEY--'}

        response = c.post('/keyserver/user/activate', pdata) 
        resp = json.loads(response.content)
        self.assertEquals(resp['resultcode'], 1)
        

    def test_getpubkey(self):
        c = Client()
        sessid = self._auth()
        pdata = {'sessionid': sessid, 'uid': '4b655fff-c043-45b9-b864-7b3a6d26aec3'}
        response = c.post('/keyserver/pubkey/get', pdata)
        resp = json.loads(response.content)
        assert(resp['pubkey'] != None)

    def test_pubmessage(self):
        c = Client()
        sessid = self._auth()
        pdata = {'sessionid': sessid, 'uid': '4b655fff-c043-45b9-b864-7b3a6d26aec3'}
        pdata['uid'] = '3639a22b-9280-4603-8a98-467fdc6662f2'
        pdata['msg'] = 'enc message'
        response = c.post('/keyserver/message/send', pdata)
        resp = json.loads(response.content)
        self.assertEquals(resp['success'], 1)

    def test_getmessage(self):
        c = Client()
        sessid = self._auth()
        pdata = {'sessionid': sessid, 'uid': '4b655fff-c043-45b9-b864-7b3a6d26aec3'}
        pdata['uid'] = '3639a22b-9280-4603-8a98-467fdc6662f2'
        pdata['msg'] = 'enc message'
        response = c.post('/keyserver/message/send', pdata)
        resp = json.loads(response.content)
        self.assertEquals(resp['success'], 1)

        pdata = {'sessionid': sessid, 'msgid': resp['msgid']}
        response = c.post('/keyserver/message/get', pdata)
        resp = json.loads(response.content)
        self.assertEquals(1, resp['found'])

    def test_pubenckey(self):
        c = Client()
        sessid = self._auth()
        pdata = {'sessionid': sessid, 'uid': '4b655fff-c043-45b9-b864-7b3a6d26aec3'}
        pdata['uid'] = '3639a22b-9280-4603-8a98-467fdc6662f2'
        pdata['msg'] = 'enc message'
        response = c.post('/keyserver/message/send', pdata)
        resp = json.loads(response.content)
        self.assertEquals(resp['success'], 1)

        fdata = { 'sessionid': sessid, 'msgid': resp['msgid'], 'key': 'abcdef', 'mintoexpire': '3' }
        response = c.post('/keyserver/msgkey/send', fdata)
        resp = json.loads(response.content)
        self.assertEquals(1, resp['resultcode'])

    def test_listcontacts(self):
        c = Client()
        sessid = self._auth()
        pdata = {'sessionid': sessid}
        response = c.post('/keyserver/contacts/get', pdata)
        resp = json.loads(response.content)
        self.assertEquals(1, len(resp['contacts']))
