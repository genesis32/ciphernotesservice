# Create your views here.

from django.http import HttpResponse, Http404
from django.contrib.auth import logout
from forms import AuthRequestForm
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_protect

from core.models import User

def index(request):
    t = loader.get_template('web/index.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

@login_required
@csrf_protect
def authrequest(request):
    mu = User.objects.filter(organization=request.user.get_profile().organization)
    if request.method == 'POST':
        form = AuthRequestForm(request.POST, mobile_user=mu)
        if form.is_valid():
            pass
    else:
        form = AuthRequestForm(mobile_user=mu)

    c = RequestContext(request, {'user': request.user, 'form': form})
    return render_to_response('web/authrequest.html', c)
   
@login_required
def profile(request):
    t = loader.get_template('web/profile.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

def logout_view(request):
    logout(request)
    return redirect('/')
