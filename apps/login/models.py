from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def validate_reg(self, postData):
        errors = {}
        for field, value in postData.iteritems():
            if len(value) < 1:
                errors[field] = 'All Fields are Required'
        if 'email' not in errors and not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = 'Invalid Email'
        if 'email' not in errors and len(self.filter(email=postData['email'])) > 0:
            errors['email'] = 'Email already in use'
        if 'password' not in errors and len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 Characters'
        if 'password' not in errors and postData['password'] != postData['confirm']:
            errors['password'] = 'Passwords do not match'
        if postData['birthday'] >= datetime.date.today().strftime('%Y-%m-%d'):
            errors['birtday'] = 'Birthday must be in the past'
        if len(errors) == 0:
            hashed = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            new_user = self.create(
                name=postData['name'],
                email=postData['email'],
                password=hashed,
                birthday=postData['birthday']
            )
            return new_user
        else:
            return errors

    def validate_login(self, postData):
        errors = {}
        if len(self.filter(email = postData['email'])) > 0:
            user = self.filter(email = postData['email'])[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = 'Incorrect Password'
        else:
            errors['email'] = 'Incorrect Email'
        if errors:
            return errors
        return user

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateTimeField()
    objects = UserManager()
    def __repr__(self):
        return 'User: {}'.format(self.name)
