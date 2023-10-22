from django.contrib.sites.shortcuts import get_current_site
from django. contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from OnlineFood_main import settings


def detectUser(user):
    if user.role == 2:
        redirectUrl = 'venDashbord'
        return redirectUrl
    elif user.role == 1:
        redirectUrl = 'custDashbord'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
    
def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template,{
        'user' : user,   #user
        'domain': current_site, #get the domain
        'uid': urlsafe_base64_encode(force_bytes(user.pk)), #get user primery key
        'token': default_token_generator.make_token(user), #make token for user
        
    })
    
    to_email = user.email
    mail = EmailMessage(mail_subject, message, to=[to_email])
    mail.send()
    
    

    