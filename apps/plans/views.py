from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import *
from ..login.models import User
from django.contrib.messages import error
import datetime

def home(request):
    if 'user_id' not in request.session.keys():
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    todays_apps = user.appointments.filter(date=datetime.date.today()).order_by('time')
    future_apps = user.appointments.exclude(date=datetime.date.today()).order_by('date').order_by('time')
    context = {
        'date': datetime.date.today(),
        'user': user,
        'todays_apps': todays_apps,
        'future_apps': future_apps
    }
    return render(request, 'plans/index.html', context)

def create(request):
    result = Appointment.objects.validate_app(request.POST, request.session['user_id'])
    if type(result) == dict:
        for tag, message in result.iteritems():
            error(request, message, extra_tags=tag)
    return redirect('/appointments')


def edit(request, app_id):
    if 'user_id' not in request.session.keys():
        return redirect('/')
    appointment = Appointment.objects.get(id=app_id)
    context = {
        'appointment': Appointment.objects.get(id=app_id),
        'time': appointment.time.strftime('%H:%M:%S')
    }
    return render(request, 'plans/edit.html', context)

def update(request, app_id):
    result = Appointment.objects.validate_update(request.POST, request.session['user_id'])
    if len(result):
        for tag, message in result.iteritems():
            error(request, message, extra_tags=tag)
        return redirect('/appointments/{}/edit'.format(app_id))
    update_app = Appointment.objects.get(id=app_id)
    update_app.task = request.POST['task']
    update_app.status = request.POST['status']
    update_app.date = request.POST['date']
    update_app.time = request.POST['time']
    update_app.save()
    return redirect('/appointments')

def delete(request, app_id):
    Appointment.objects.get(id=app_id).delete()
    return redirect(reverse('home'))
