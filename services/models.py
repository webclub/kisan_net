from django.db import models,connection
from django.contrib.auth.models import User
from jsonfield import JSONField
from datetime import datetime
import json

class PostManager(models.Manager):
	# need to optimise this method as traversing the complete tables again and again ain't good
	# also see if JOIN is possible but take care of null values
	def cmp(a,b):
		# custom compare function for result list sort
		return (a['distance'] < b['distance']) or (a['distance']==b['distance'] and datetime(a['timestamp']) > datetime(b['timestamp']))

	def nearby_put_posts(self, longitude, latitude, use_miles=False):
		if use_miles:
			distance_unit = 3959
		else:
			distance_unit = 6371

		cursor = connection.cursor()
		print longitude,latitude
		sql = """SELECT user_id,((%f * acos( cos( radians(%f) ) * cos( radians( latitude ) ) *
			cos( radians( longitude ) - radians(%f) ) + sin( radians(%f) ) * sin( radians( latitude ) ) ) ) ) AS distance FROM services_userprofile ORDER BY distance ASC
			""" % (distance_unit, latitude, longitude, latitude)
		cursor.execute(sql)
		ids = {}
		for row in cursor.fetchall():
			ids[row[0]] = row[1]

		posts = put_requests.objects.all()
		result = [
			{'user':{'name':post.user.get_full_name(),'id':post.user_id},
			'distance':ids[post.user_id],
			'post':{'message':post.message,'image':post.photo.url if post.photo else None},
			'timestamp':post.timestamp} for post in posts]		
		result.sort(cmp)
		# print 'CHECK'*5
		for i in range(len(result)):
			result[i]['timestamp'] = str(result[i]['timestamp'])
		return result
	
	def nearby_get_posts(self, longitude, latitude, use_miles=False):
		if use_miles:
			distance_unit = 3959
		else:
			distance_unit = 6371

		cursor = connection.cursor()
		print longitude,latitude
		sql = """SELECT user_id,((%f * acos( cos( radians(%f) ) * cos( radians( latitude ) ) *
			cos( radians( longitude ) - radians(%f) ) + sin( radians(%f) ) * sin( radians( latitude ) ) ) ) ) AS distance FROM services_userprofile ORDER BY distance ASC
			""" % (distance_unit, latitude, longitude, latitude)
		cursor.execute(sql)
		ids = {}
		for row in cursor.fetchall():
			ids[row[0]] = row[1]

		posts = get_requests.objects.all()
		result = [
			{'user':{'name':post.user.get_full_name(),'id':post.user_id},
			'distance':ids[post.user_id],
			'post':{'message':post.message,'image':post.photo.url if post.photo else None},
			'timestamp':str(post.timestamp)} for post in posts]		
		result.sort(cmp)
		return result


class UserProfile(models.Model):
	user = models.ForeignKey(User, unique = True)
	dob = models.DateField(blank = True, null = True)
	location = JSONField(null = True)
	longitude = models.FloatField(null = True)
	latitude = models.FloatField(null = True)
	phone = models.CharField(db_index = True,max_length = 10)
	token = models.CharField(max_length = 40,db_index = True)
	crops = JSONField(null = True)
	profile_pic = models.ImageField(upload_to = 'profile_pictures' ,max_length = 150,null = True)
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

class put_requests(models.Model):
	user = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now_add = True)
	message = JSONField()
	photo = models.ImageField(upload_to = 'put_photos' ,max_length = 150,null = True)
	objects = PostManager()

class get_requests(models.Model):
	user = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now_add = True)
	message = JSONField()
	photo = models.ImageField(upload_to = 'get_photos' ,max_length = 150,null = True)
	objects = PostManager()