from django.template import Context, loader
from django.http import HttpResponse

def index(request):
    t = loader.get_template('keyserver/index.html')
    c = Context({})
    return HttpResponse(t.render(c))

def activate(request, activation_id):
    return HttpResponse('activation id %s' % (activation_id))
