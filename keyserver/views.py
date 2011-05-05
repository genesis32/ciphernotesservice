import json
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from models import Device, User, Message, Key, UserAssociation
from statuscodes import StatusCodes

def index(request):
    t = loader.get_template('keyserver/index.html')
    c = Context({})
    return HttpResponse(t.render(c))

@csrf_exempt
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
    return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
@csrf_exempt
def getmessage(request, msgid):
    response_data = {}
    try:
        msg = Message.objects.get(pk=msgid)
        response_data['resultcode'] = StatusCodes.MessageFound
        response_data['msg'] = msg.enc_msg
    except Message.DoesNotExist:
        response_data['resultcode'] = StatusCodes.MessageNotFound

    return HttpResponse(json.dumps(response_data), mimetype="application/json")
        
@csrf_exempt
def sendmessage(request):
    response_data = {}
    if request.method == 'POST':
        toid = request.POST['toid']
        frid = request.POST['frid']
        try:
            toUser = User.objects.get(pk=toid)
            frUser = User.objects.get(pk=frid)
            msg  = request.POST['msg']

            m = Message(from_user=frUser, to_user=toUser, enc_msg=msg)
            m.save()
            response_data['msgid']      = m.id
            response_data['resultcode'] = StatusCodes.MessageSent
        except User.DoesNotExist:
            response_data['resultcode'] = StatusCodes.MessageSendFailedInvalidUser

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def sendmsgkey(request):
    response_data = {}
    if request.method == 'POST':
        msgid = request.POST['msgid']
        enckey = request.POST['key']
        try:
            msg = Message.objects.get(pk=msgid)
            k = Key(message=msg, key=enckey)
            k.save()
            response_data['resultcode'] = StatusCodes.KeySent
        except Message.DoesNotExist:
            response_data['resultcode'] = StatusCodes.KeySendFailedMessageNotFound

    return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
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

    return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def activate(request, udid):
    response_data = {}
    if request.method == 'POST':
        try:
            d = Device.objects.get(udid=udid)
            ls = request.raw_post_data.split('=', 1)
            d.owner.pubkey = ls[1]
            d.activated = 1
            
            d.owner.save()
            d.save()
            response_data['resultcode'] = StatusCodes.DeviceNowActivated
        except Device.DoesNotExist:
            response_data['resultcode'] = StatusCodes.DeviceNotFound

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

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

    return HttpResponse(json.dumps(response_data), mimetype="application/json")
