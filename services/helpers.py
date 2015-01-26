from datetime import datetime,date
from django.contrib.auth.models import User
from models import *

def validate_date(_date):
	# check if this date is >= today
	# else _date = now()
	if _date < datetime.now():
		_date = datetime.now()
	return _date

def give_date(dob):
	if dob:
		dob_new = datetime.strptime(dob,"%d/%m/%Y")
		print 'dob_new ' + str(dob_new)
		return dob_new
	else:
		return None

def delete_user(username):
	if username:
		User.objects.filter(username = username).delete()
	return

def rm_queue(phone):
	if phone:
		print 'removed number from queue'
		RegQueue.objects.filter(phone = phone).delete()	

	return