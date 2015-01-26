from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.exceptions import *
from functools import wraps
import json,traceback
from models import *

def user_exists(view_func):
    def _decorator(request, *args, **kwargs):
        # a decorator to check if the user requested exists in the database
        try:
            phone = request.POST.get('phone', None)
            user = User.objects.get(username=phone)
            token = UserProfile.objects.get(user_id= user.id)
            token = token.token
            return HttpResponse(json.dumps({'token':token,'registered':True}))
        except User.DoesNotExist:
            return view_func(request, *args, **kwargs)
    return wraps(view_func)(_decorator)

def user_authenticated(view_func):
    def _decorator(request, *args, **kwargs):
        # a decorator to check if the user requested exists in the database
        try:
            token = request.POST.get('token',None)
            user = UserProfile.objects.get(token = token)
            return view_func(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            return HttpResponse(json.dumps({'authenticated':False}))
    return wraps(view_func)(_decorator)
