from django.shortcuts import render, redirect, reverse
from .models import User
from django.contrib.messages import error

def index(request):
    return render(request, 'login/index.html')

def register(request):
    result = User.objects.validate_reg(request.POST)
    if type(result) == dict:
        for tag, message in result.iteritems():
            error(request, message, extra_tags=tag)
        return redirect('/')
    else:
        request.session['user_id'] = result.id
        return redirect('/appointments')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == dict:
        for tag, message in result.iteritems():
            error(request, message, extra_tags=tag)
        return redirect('/')
    else:
        request.session['user_id'] = result.id
        return redirect('/appointments')

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')
