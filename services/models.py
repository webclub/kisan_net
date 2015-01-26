from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique = True)
	dob = models.DateField(blank = True, null = True)
	location = JSONField()
	phone = models.CharField(db_index = True,max_length = 10)
	token = models.CharField(max_length = 40,db_index = True)
	crops = JSONField(null = True)
	time_registered = models.DateTimeField(auto_now_add=True)

class RegQueue(models.Model):
	name = models.CharField(max_length = 30,null = True)
	phone = models.CharField(max_length = 10,db_index = True)
	time_queued = models.DateTimeField(auto_now_add = True)

class LabourRequests(models.Model):
	user = models.ForeignKey(User,unique = True,db_index = True)
	count = models.IntegerField(default = 0)
	from_date = models.DateField(null = True)
	to_date = models.DateField(null = True)
	fulfilled = models.BooleanField(default = False)
	time_queued = models.DateTimeField(auto_now_add = True)
