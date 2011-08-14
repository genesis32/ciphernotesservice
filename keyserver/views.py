import simplejson as json
from datetime import datetime, timedelta

from django.http import HttpResponse, Http404
from django.template import Context, loader

from models import Device, User, Message, Key, UserAssociation
from statuscodes import StatusCodes
from utils import get_http_post_params

def render_to_json(results):
    return HttpResponse(json.dumps(results), mimetype='application/json')

def index(request):
    t = loader.get_template('keyserver/index.html')
    c = Context({})
    return HttpResponse(t.render(c))

def getpubkey(request, uid):
    response_data = {}
    found = 0
    try:
       u = User.objects.get(pk=uid)
       found = 1
       response_data['pubkey'] = u.pubkey
    except User.DoesNotExist:
        pass

    response_data['found'] = found
    return render_to_json(response_data)
    
def getmessage(request, msgid):
    response_data = {}
    response_data['found'] = 0
    try:
        msg = Message.objects.get(pk=msgid)
        response_data['found'] = 1
        response_data['msg'] = msg.enc_msg
    except Message.DoesNotExist:
        pass

    return render_to_json(response_data)
        
def sendmessage(request):
    response_data = {}
    if request.method == 'POST':
        kv = get_http_post_params(request.raw_post_data)
        toid = kv['toid']
        frid = kv['frid']
        try:
            toUser = User.objects.get(pk=toid)
            frUser = User.objects.get(pk=frid)
            msg  = kv['msg']

            m = Message(from_user=frUser, to_user=toUser, enc_msg=msg)
            m.save()
            response_data['msgid']      = m.id
            response_data['resultcode'] = StatusCodes.MessageSent
        except User.DoesNotExist:
            response_data['resultcode'] = StatusCodes.MessageSendFailedInvalidUser

        return render_to_json(response_data)
    
def getmsgkey(request, msgid):
    response_data = {}
    response_data['found'] = 0
    try:
        msg = Message.objects.get(pk=msgid)
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
    response_data = {}
    if request.method == 'POST':
        kv = get_http_post_params(request.raw_post_data)
        msgid = kv['msgid']
        enckey = kv['key']
        min_to_expire = int(kv['mintoexpire'])
        print min_to_expire
        try:
            msg = Message.objects.get(pk=msgid)
            k = Key(message=msg, key=enckey, min_to_expire=min_to_expire)
            k.save()
            response_data['resultcode'] = StatusCodes.KeySent
        except Message.DoesNotExist:
            response_data['resultcode'] = StatusCodes.KeySendFailedMessageNotFound

    return render_to_json(response_data)

def getcontacts(request, udid):
    response_data = {'contacts': []}

    try:
        d = Device.objects.get(udid=udid)
        ua1 = UserAssociation.objects.filter(user1=d.owner)
        for ua in ua1:
            rdata = (ua.user2.id, ua.user2.email)
            response_data['contacts'].append(rdata)

        ua2 = UserAssociation.objects.filter(user2=d.owner)
        for ua in ua2:
            rdata = (ua.user1.id, ua.user1.email)
            response_data['contacts'].append(rdata)

    except Device.DoesNotExist:
        pass

    return render_to_json(response_data)

def activate(request, udid):
    response_data = {}
    if request.method == 'POST':
        kv = get_http_post_params(request.raw_post_data)
        try:
            d = Device.objects.get(udid=udid)

            d.owner.pubkey = kv['pubkey']
            d.activated = 1
            
            d.owner.save()
            d.save()
            response_data['resultcode'] = StatusCodes.DeviceNowActivated
        except Device.DoesNotExist:
            response_data['resultcode'] = StatusCodes.DeviceNotFound

        return render_to_json(response_data)

def activated(request, udid):
    response_data = {}
    try:
        d = Device.objects.get(udid=udid)
        if d.activated == 1:
            response_data['resultcode'] = StatusCodes.DeviceIsActivated
        else:
            response_data['resultcode'] = StatusCodes.DeviceIsNotActivated

    except Device.DoesNotExist:
        response_data['resultcode'] = StatusCodes.DeviceNotFound

    return render_to_json(response_data)
