from __future__ import unicode_literals
from ..login.models import User
from django.db import models
import datetime

class AppointmentManager(models.Manager):
    def validate_app(self, postData, user_id):
        errors = {}
        for field, value in postData.iteritems():
            if len(value) < 1:
                errors[field] = 'All Fields are Required'
        if postData['date'] < datetime.date.today().strftime('%Y-%m-%d'):
            errors['date'] = 'Appointment cannot be in the past'
        if 'date' not in errors and len(self.filter(date=postData['date'])) > 0:
            if 'time' not in errors and len(self.filter(time=postData['time'])) > 0:
                errors['time'] = 'You already have an Appointment at that time'
        if len(errors) == 0:
            self.create(
                task = postData['task'],
                date = postData['date'],
                time = postData['time'],
                user = User.objects.get(id=user_id)
            )
        else:
            return errors

    def validate_update(self, postData, user_id):
        errors = {}
        for field, value in postData.iteritems():
            if len(value) < 1:
                errors[field] = 'All Fields are Required'
        if postData['date'] < datetime.date.today().strftime('%Y-%m-%d'):
            errors['date'] = 'Appointment cannot be in the past'
        if 'date' not in errors and len(self.filter(date=postData['date'])) > 0:
            if 'time' not in errors and len(self.filter(time=postData['time'])) > 0:
                errors['time'] = 'You already have an Appointment at that time'
        return errors

class Appointment(models.Model):
    task = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default='Pending')
    date = models.DateField()
    time = models.TimeField()
    user = models.ForeignKey(User, related_name='appointments')
    objects = AppointmentManager()
    def __repr__(self):
        return 'Task scheduled for {}'.format(self.user.name)
