import json
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from models import Device, User, Message
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

            response_data['resultcode'] = StatusCodes.MessageSent
        except User.DoesNotExist:
            response_data['resultcode'] = StatusCodes.MessageSendFailedInvalidUser

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def activate(request, udid):
    response_data = {}
    if request.method == 'POST':
        try:
            d = Device.objects.get(udid=udid)
            d.owner.pubkey = request.POST['pubkey']
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
