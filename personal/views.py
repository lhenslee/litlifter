from django.shortcuts import render
from membership.models import Account

content = {}
content['profile'] = 'Login'
content['signup'] = 'Sign Up'
content['signlink'] = '/membership/create/'
content['profilelink'] = '/membership/login/'

def index(request):
    try:
        user = Account.objects.get(username=request.session['member'])
        content['profile'] = user.username.capitalize()
        content['signup'] = 'Logout'
        content['signlink'] = '/membership/profile/'
        content['profilelink'] = '/membership/profile/'
    except Exception: pass
    return render(request, 'handmade/home.html', content)

def contact(request):
    return render(request, 'personal/basic.html', {'info':
                                                   ['If you would like to contact me, please email me',
                                                    'tennhamme@gmail.com']})
