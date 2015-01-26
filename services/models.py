from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique = True)
	dob = models.DateField(blank = True, null = True)
	location = JSONField(null = True)
	longitude = models.FloatField(null = True)
	latitude = models.FloatField(null = True)
	phone = models.CharField(db_index = True,max_length = 10)
	token = models.CharField(max_length = 40,db_index = True)
	crops = JSONField(null = True)
	profile_pic = models.ImageField(upload_to = 'profile_pictures/%d'%self.id ,max_length = 150,null = True)
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
	user = models.ManyToManyField(User)
	timestamp = models.DateTimeField(auto_now_add = True)
	message = JSONField()
	photo = models.ImageField(upload_to = 'put_photos/%d'%self.id ,max_length = 150)

	# need to optimise this method as traversing the complete tables again and again ain't good
	# also see if JOIN is possible but take care of null values
	def nearby_posts(self, longitude, latitude, use_miles=False):
		if use_miles:
			distance_unit = 3959
		else:
			distance_unit = 6371

		cursor = connection.cursor()

		sql = """SELECT user_id, latitude, longitude FROM services_userprofile ORDER BY (%f * acos( cos( radians(%f) ) * cos( radians( latitude ) ) *
			cos( radians( longitude ) - radians(%f) ) + sin( radians(%f) ) * sin( radians( latitude ) ) ) ) ASC
			""" % (distance_unit, latitude, longitude, latitude)
		cursor.execute(sql)
		ids = [row[0] for row in cursor.fetchall()]

		return self.filter(user_id__in=ids)

class get_requests(models.Model):
	user = models.ManyToManyField(User)
	timestamp = models.DateTimeField(auto_now_add = True)
	message = JSONField()
	photo = models.ImageField(upload_to = 'get_photos/%d'%self.id ,max_length = 150,null = True)
