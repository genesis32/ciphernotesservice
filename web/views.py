# Create your views here.

import cncrypto
import uuid
import urllib
import base64

from django.http import HttpResponse, Http404
from django.contrib.auth import logout
from forms import AuthRequestForm
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_protect
from django.core.mail import EmailMessage

from core.models import User, Message, Key

def index(request):
    t = loader.get_template('web/index.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

def create_authmsg(request, to_user, authcode):
    from_org = request.user.get_profile().organization
    subject = "Auth request from %s" % (from_org.name)
    headers = { 'Type': 'AUTHCODE', 'Subject': subject, 'FromName': from_org.name } 
    body = ''
    for k, v in headers.items():
        body += '%s:%s\r\n' % (k, v)
    body += '\r\n'        
    body += authcode

    return body

def save_msg(request, to_user, auth_code):
    
    authmsg = create_authmsg(request, to_user, auth_code)

    aeskeyp1, aeskeyp2, cphr_authmsg = cncrypto.aes_encrypt_authcode(authmsg)
    cphr_aeskeyp1 = cncrypto.rsa_encrypt_aeskey(to_user.pubkey, aeskeyp1)

    msg = Message()
    msg.from_org=request.user.get_profile().organization
    msg.to_user = to_user
    msg.sysid   = str(uuid.uuid4())
    msg.enc_msg = cphr_authmsg 
    msg.save()

    key = Key()
    key.message = msg
    key.sysid   = str(uuid.uuid4())
    key.key     = cphr_aeskeyp1
    key.min_to_expire = 1
    key.save()

    from_email = "noreply@ciphernotes.com"
    subject = "Auth code request"
    body = """
<a href="secdef://%s/%s">Tap Here</a> to get your authentication code.
""" % (msg.sysid, urllib.quote_plus(base64.b64encode(aeskeyp2)))

    print body

    email_msg = EmailMessage(subject, body, from_email, [to_user.email])
    email_msg.content_subtype = "html"
    email_msg.send()

@login_required
@csrf_protect
def authrequest(request):
    mu = User.objects.filter(organization=request.user.get_profile().organization, activated=True)
    if request.method == 'POST':
        form = AuthRequestForm(request.POST, mobile_user=mu)
        if form.is_valid():
            to_user = form.cleaned_data['mobile_user']
            auth_code = form.cleaned_data['authorization_code']
            save_msg(request, to_user, auth_code)
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
