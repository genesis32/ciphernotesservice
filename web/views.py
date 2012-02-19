# Create your views here.

from django.http import HttpResponse, Http404
from django.contrib.auth import logout
from forms import SetupForm
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_protect

def index(request):
    t = loader.get_template('web/index.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

@login_required
@csrf_protect
def setup(request):
    if request.method == 'POST':
        form = SetupForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = SetupForm()

    c = RequestContext(request, {'user': request.user, 'form': form})
    return render_to_response('web/setup.html', c)

@login_required
def profile(request):
    t = loader.get_template('web/profile.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

def logout_view(request):
    logout(request)
    return redirect('/')
