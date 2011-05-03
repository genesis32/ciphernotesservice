import json
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def index(request):
    t = loader.get_template('keyserver/index.html')
    c = Context({})
    return HttpResponse(t.render(c))

@csrf_exempt
def activate(request, activation_id):
    response_data = {}
    if request.method == 'POST':
        response_data['result'] = 'success'
        response_data['pubkey'] = request.POST['pubkey']
        response_data['activation_id'] = activation_id
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

def registered(request, udid):
    response_data = {}
    response_data['result'] = 'registered'
    response_data['message'] = 'The message'
    return HttpResponse(json.dumps(response_data), mimetype="application/json")
