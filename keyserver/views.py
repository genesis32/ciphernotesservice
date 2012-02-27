import json
import uuid
from datetime import datetime, timedelta

from django.http import HttpResponse, Http404
from django.template import Context, loader

from core.models import User, Message, Key, UserAssociation
from models import UserSession

def auth_session(request):
    if not request.POST.has_key('sessionid'):
        return None

    sessionid = request.POST['sessionid']
    try:
        session = UserSession.objects.get(session_id=sessionid)
        return session.user 
    except UserSession.DoesNotExist:
        pass
        
    return None 

def logout_session(request):
    if not request.POST.has_key('sessionid'):
        raise

    sessionid = request.POST['sessionid']
    session = UserSession.objects.filter(session_id=sessionid)
    session.delete()

    response_data = {'status': 'ok'}
    return render_to_json(response_data)

def render_to_json(results):
    return HttpResponse(json.dumps(results), mimetype='application/json')

def auth(request):
    response_data = {}
    success = 0
    if request.method == 'POST':
        uemail = request.POST['email']

        # TODO: Encrypt PIN.
        upin   = request.POST['pin']
         
        try:
            u = User.objects.get(email=uemail, pin=upin)
            existing_session = UserSession.objects.filter(user=u)
            if len(existing_session) == 0:
                sessionid = str(uuid.uuid4())
             
                us = UserSession()
                us.user = u
                us.session_id = sessionid
                us.save()
                response_data['sessionid'] = sessionid
                response_data['userid']    = u.sysid
            else:
                response_data['sessionid'] = existing_session[0].session_id
                response_data['userid']    = u.sysid

            success = 1
        except User.DoesNotExist:
            pass

    response_data['success'] = success 
    return render_to_json(response_data)
        
def getuserprofile(request):
    cu = auth_session(request) 
    if cu == None:
        raise
   
    response_data = { 'name': cu.name, 'email': cu.email }

    return render_to_json(response_data)

def index(request):
    t = loader.get_template('keyserver/index.html')
    c = Context({})
    return HttpResponse(t.render(c))

def getpubkey(request):
    cu = auth_session(request) 
    if cu == None:
        raise

    response_data = {}
    found = 0
    try:
       u = User.objects.get(sysid=request.POST['uid'])
       found = 1
       response_data['pubkey'] = u.pubkey
    except User.DoesNotExist:
        pass

    response_data['found'] = found
    return render_to_json(response_data)
    
def getmessage(request):
    cu = auth_session(request) 
    if cu == None:
        raise

    response_data = {}
    response_data['found'] = 0
    try:
        msg = Message.objects.get(sysid=request.POST['msgid'])
        response_data['found'] = 1
        response_data['msg'] = msg.enc_msg
    except Message.DoesNotExist:
        pass

    return render_to_json(response_data)
        
def sendmessage(request):
    cu = auth_session(request) 
    if cu == None:
        raise
    
    response_data = {}
    response_data['success'] = 0
    try:
        toUser = User.objects.get(sysid=request.POST['uid'])
        msg    = request.POST['msg']
        
        msysid = str(uuid.uuid4())
        m = Message(from_user=cu, to_user=toUser, enc_msg=msg, sysid=msysid)
        m.save()
        response_data['msgid']   = msysid 
        response_data['success'] = 1
    except User.DoesNotExist:
        pass

    return render_to_json(response_data)
    
def getmsgkey(request):
    cu = auth_session(request) 
    if cu == None:
        raise

    response_data = {}
    response_data['found'] = 0
    try:
        msg = Message.objects.get(sysid=request.POST['msgid'])
        k   = Key.objects.get(message=msg)
        response_data['found'] = 1
        response_data['msgkey'] = k.key
        if k.min_to_expire > 0:
            k.expires = datetime.utcnow() + timedelta(minutes=k.min_to_expire)
            k.save()
        else:
            k.delete()
    except Message.DoesNotExist:
        pass
    except Key.DoesNotExist:
        pass

    return render_to_json(response_data)

def sendmsgkey(request):
    cu = auth_session(request) 
    if cu == None:
        raise

    response_data = {}
    try:
        min_to_expire = int(request.POST['mintoexpire'])
        msg = Message.objects.get(sysid=request.POST['msgid'])
        msysid = str(uuid.uuid4())
        k = Key(message=msg, key=request.POST['key'], min_to_expire=min_to_expire, sysid=msysid)
        k.save()
        response_data['resultcode'] = 1
    except Message.DoesNotExist:
        response_data['resultcode'] = 0

    return render_to_json(response_data)

def getcontacts(request):
    cu = auth_session(request) 
    if cu == None:
        raise

    response_data = {'contacts': []}
    ua1 = UserAssociation.objects.filter(user1=cu)
    for ua in ua1:
        if(ua.user2.activated): 
            rdata = (ua.user2.sysid, ua.user2.email)
            response_data['contacts'].append(rdata)

    ua2 = UserAssociation.objects.filter(user2=cu)
    for ua in ua2:
        if(ua.user1.activated): 
            rdata = (ua.user1.sysid, ua.user1.email)
            response_data['contacts'].append(rdata)

    return render_to_json(response_data)

def activate(request):
    cu = auth_session(request) 
    if cu == None:
        raise

    response_data = {}
    cu.pubkey = request.POST['pubkey']
    cu.activated = True
    cu.save()
    response_data['resultcode'] = 1 

    return render_to_json(response_data)

def activated(request):
    cu = auth_session(request) 
    if cu == None:
        raise

    response_data = {'resultcode': int(cu.activated)}

    return render_to_json(response_data)
