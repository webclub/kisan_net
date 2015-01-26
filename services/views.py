from django.shortcuts import render
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from models import *
from django.contrib.auth.models import User
import urllib,json
from decorators import *
from helpers import *
import traceback
import md5

@csrf_exempt
@require_POST
@user_exists
def register(request):
	# read data from the form and register a user
	# send back a token as response
	# if there is any conflicting field send err in response
	# for users registering through call, check a post param
	# if the param call is set , remove the entry from RegQueue
	try:
		first_name = request.POST['first_name']
		last_name = request.POST.get('last_name',None)
		email = request.POST.get('email',None)
		phone = request.POST.get('phone',None)
		user = User.objects.create_user(username = phone,email = email,first_name = first_name, last_name = last_name,password = phone[::-1])
	except:
		print traceback.format_exc()
		return HttpResponse(json.dumps({'registered':False,'user_obj':False,'success':False}))
	try:
		dob = give_date(request.POST.get('dob',None))
		longitude = request.POST.get('longitude',None)
		latitude = request.POST.get('latitude',None)
		location_name = request.POST.get('location_name',None)
		location = json.dumps({'longitude':longitude,'latitude':latitude,'location_name':location_name})
		token = md5.new(phone[::-1]+str(user.id)).hexdigest()
		profile = UserProfile.objects.create(user_id = user.id,dob = dob,phone = phone,location = location,token = token)
	except:
		print traceback.format_exc()
		return HttpResponse(json.dumps({'registered':False,'user_obj':True,'success':False}))
	if request.POST.get('fromCall',None):
		rm_queue(phone)
	return HttpResponse(json.dumps({'registered':True,'token':token,'success':True}))

@csrf_exempt
@require_POST
@user_exists
def queue_reg(request):
	# add the number to db for reg by telephone
	try:
		name = request.POST.get('name',None)
		phone = request.POST.get('phone',None)
		RegQueue.objects.create(name = name,phone = phone)
		return HttpResponse(json.dumps({'queued':True,'success':True}))
	except:
		print traceback.format_exc()
		return HttpResponse(json.dumps({'success':False}))

@require_POST
@csrf_exempt
@user_authenticated
def asklabour(request):
	# receive user token,count,duration 
	# check validity of dates
	# insert a labour request in LabourRequests
	# return a request no.
	try:
		count = int(request.POST['count'])
		token = request.POST['token']
		from_date = validate_date(give_date(request.POST.get('from',None)))
		to_date = validate_date(give_date(request.POST.get('to',None)))
		if from_date > to_date:
			# swap the two
			from_date,to_date = to_date,from_date
		user = UserProfile.objects.get(token = token)
		user = user.user_id
		request_no = LabourRequests.objects.create(user_id = user,count = count,from_date = from_date,to_date = to_date)
		return HttpResponse(json.dumps({'request_no':request_no.id,'success':True}))
	except:
		print traceback.format_exc()
		return HttpResponse(json.dumps({'success':False}))

@require_POST
@csrf_exempt
@user_authenticated
def listlabour(request):
	# receive token 
	# return list of labour requests
	# JSON response {id,count,from,to}
	try:
		token = request.POST['token']
		user = UserProfile.objects.get(token = token)
		labour_requests = LabourRequests.objects.filter(user_id = user.user_id)
		result = []
		for labour_request in labour_requests:
			record = {
						'id':labour_request.id,
						'count':labour_request.count,
						'from_date':labour_request.from_date,
						'to_date':labour_request.to_date,
						'fulfilled':labour_request.fulfilled
						'timestamp':labour_request.time_queued
					 }
			result.append(record)
		print json.dumps(result,indent = 4)
		return HttpResponse(json.dumps({'LabourList':result,'success':True}))
	except:
		print traceback.format_exc()
		return HttpResponse(json.dumps({'success':False}))

@require_POST
@csrf_exempt
@user_authenticated
def editlabour(request):
	try:
		token = request.POST['token']
		user = UserProfile.objects.get(token = token)
		request_no = request.POST['request_no']
		labour_request = LabourRequests.objects.get(id = request_no)
		if labour_request.user_id == user.user_id:
			# validating if the user is original one
			count = int(request.POST['count'])
			token = request.POST['token']
			from_date = validate_date(give_date(request.POST.get('from',None)))
			to_date = validate_date(give_date(request.POST.get('to',None)))
			if from_date > to_date:
				# swap the two
				from_date,to_date = to_date,from_date
			# update record
			labour_request.count = count
			labour_request.from_date = from_date
			labour_request.to_date = to_date
			labour_request.save()
			return HttpResponse(json.dumps({'updated':True,'success':True}))
		else:
			return HttpResponse(json.dumps({'success':False}))
	except:
		print traceback.format_exc()
		return HttpResponse(json.dumps({'success':False}))

@require_POST
@csrf_exempt
def del_debug(request):
	# just for debugging purposes
	# used to delete pre mature registrations
	delete_user(request.POST['phone'])
	return HttpResponse('User deleted')
