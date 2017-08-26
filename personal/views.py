from django.shortcuts import render

def index(request):
    return render(request, 'handmade/home.html')

def contact(request):
    return render(request, 'personal/basic.html', {'info':
                                                   ['If you would like to contact me, please email me',
                                                    'tennhamme@gmail.com']})
