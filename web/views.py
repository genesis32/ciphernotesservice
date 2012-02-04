# Create your views here.

from django.http import HttpResponse, Http404
from django.template import RequestContext, loader

def index(request):
    t = loader.get_template('web/index.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

