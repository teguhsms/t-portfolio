# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, RequestContext, Template
from django.core import urlresolvers
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from django.contrib import auth
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth import authenticate, login
from django.utils.encoding import smart_str, smart_unicode

from portal.models import *
from google.appengine.api import files, urlfetch, blobstore, images, mail
from google.appengine.ext import webapp
from google.appengine.api import channel
from google.appengine.api import users

import zipfile
import simplejson
import difflib
import random
import string
import hashlib
import base64
import os
import re
import calendar
import getpass

from time import localtime
from datetime import datetime, timedelta

def main(request):
	logoData = Logo.objects.all()
	skillData = Skill.objects.all()
	aboutData = About.objects.all()
	return render_to_response('main.html', locals(), context_instance=RequestContext(request))


def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

def signin(request):
	if request.POST:
		username = request.POST.get('uname')
		password = request.POST.get('passwd')
		try:
			cek_auth = auth.authenticate(username=username, password=password)
			auth.login(request, cek_auth)
		except Exception, e:
			json_data = {'alert': "The username and password you entered is incorrect. !!", 'link': 'login', 'err': str(e)}
			return HttpResponse(simplejson.dumps(json_data), content_type="application/json")
		else:
			json_data = {'alert': 'Login success!!', 'link': 'index2', 'err': 'tidak error'}
			return HttpResponse(simplejson.dumps(json_data), content_type="application/json")
	return render_to_response('signin.html', locals(), context_instance=RequestContext(request))

def signup(request):
	if request.POST:
		username = request.POST.get('uname')
		email = request.POST.get('email')
		password = request.POST.get('passwd')
		first_name = request.POST.get('fname')
		last_name = request.POST.get('lname')
		if User.objects.filter(username=username):
			json_data = {'alert': 'Sorry, username ' + username + 'has been used!!', 'val': False}
			return HttpResponse(simplejson.dumps(json_data), content_type="application/json")
		usr = User.objects.create_user(username=username, password=password,
		                               email=email)  # 3 atribut penting u/ create_user
		usr.first_name = first_name
		usr.last_name = last_name
		usr.save()
		json_data = {'alert': 'Register success!!'}
		return HttpResponse(simplejson.dumps(json_data), content_type="application/json")
	return render_to_response('signup.html', locals(), context_instance=RequestContext(request))


def login(request):
	if request.POST.get('action') == 'submit':
		username = request.POST.get('uname')
		password = request.POST.get('passwd')
		try:
			cek_auth = auth.authenticate(username=username, password=password)
			auth.login(request, cek_auth)
		except Exception, e:
			json_data = {'alert': "Some information you entered doesn't look right.!!", 'link': 'login', 'err': str(e)}
			return HttpResponse(simplejson.dumps(json_data), content_type="application/json")
		else:
			json_data = {'alert': 'Login success!!', 'link': 'index2', 'err': 'tidak error'}
			return HttpResponse(simplejson.dumps(json_data), content_type="application/json")
	return render_to_response('login.html', locals(), context_instance=RequestContext(request))

def admin(request):
	return render_to_response('admin_panel/admin.html', locals(), context_instance=RequestContext(request))

def about(request):
	aboutData = About.objects.all()
	if request.POST.get('action') == 'about':
		countDat = About.objects.all().count()
		#save data if aboutData == 0
		name = request.POST.get('name')
		dob = request.POST.get('dob')
		pob = request.POST.get('pob')
		profession = request.POST.get('profession')
		interests = request.POST.get('interests')
		residence = request.POST.get('residence')
		phone = request.POST.get('phone')
		email = request.POST.get('email')
		website = request.POST.get('website')
		desc = request.POST.get('desc')
		idAbout = request.POST.get('id')
		dAbout = About()
		try:
			x = About.objects.get(seqAbout=0)
		except Exception, e:
			json_data = {'alert': e}
			return HttpResponse(simplejson.dumps(json_data), content_type="application/json")
		else:
			json_data = {'alert': 'Update Data Success!!'}
			return HttpResponse(simplejson.dumps(json_data), content_type="application/json")


	elif request.POST.get('action') == 'delAbout':
		id = request.POST.get('id')
		delData = About.objects.filter(seqAbout=int(id))
		delData.delete()
		aboutData = About.objects.all()
		visibleAbout = aboutData.count()
		return render_to_response('admin-panel/skill_table.html', locals(), context_instance=RequestContext(request))

	return render_to_response('admin_panel/about.html', locals(), context_instance=RequestContext(request))
	#if request.user.is_authenticated():
	#	aboutDataData = About.objects.all()
	#	visibleAbout = aboutData.count()
	#	return render_to_response('admin_panel/about.html', locals(), context_instance=RequestContext(request))

	#return HttpResponseRedirect('/')

def main_about(request):
	user = User.objects.all()
	aboutData = About.objects.all()
	visibleAbout = aboutData.count()
	return render_to_response('main_about.html', locals(), context_instance=RequestContext(request))

def adminpanel(request):
	user = User.objects.all()
	return render_to_response('admin/admin-panel.html', locals(), context_instance=RequestContext(request))




def lockme(request):
	return render_to_response('admin-panel/modal.lockme.html', locals(), context_instance=RequestContext(request))


def index2(request):
	if request.user.is_authenticated():
		return render_to_response('admin-panel/index2.html', locals(), context_instance=RequestContext(request))
	return HttpResponseRedirect('/')

def form(request):
	if request.user.is_authenticated():
		return render_to_response('admin-panel/form.html', locals(), context_instance=RequestContext(request))
	return HttpResponseRedirect('/')

def icons(request):
	#if request.user.is_authenticated():
	return render_to_response('admin-panel/icons.html', locals(), context_instance=RequestContext(request))


def lock_screen(request):
	if request.POST.get('action') == 'submit':
		passwd = request.POST.get('passwd')
		cekPass = User.objects.get(username=request.user.username)

		if authenticate(username=request.user.username, password=passwd):
			json_data = {'result': True}
		else:
			json_data = {'result': False}
		# hasil = cekPass.password
		#json_data = {'result': hasil}
		#pw = getpass.getpass()
		#json_data = {'result': pw}
		return HttpResponse(simplejson.dumps(json_data), content_type="application/json")

	return render_to_response('admin-panel/lock_screen.html', locals(), context_instance=RequestContext(request))

def iconPop(request):
	if request.user.is_authenticated():
		logoData = Logo.objects.all()
		skillData = Skill.objects.all()
		visibleSkill = skillData.count()
		visibleLogo = logoData.count()
		return render_to_response('admin-panel/popUp/iconPop.html', locals(), context_instance=RequestContext(request))

	return HttpResponseRedirect('/')

# Content
def header(request):
	if request.user.is_authenticated():
		logoData = Logo.objects.all()
		skillData = Skill.objects.all()
		visibleSkill = skillData.count()
		visibleLogo = logoData.count()
		return render_to_response('admin-panel/header.html', locals(), context_instance=RequestContext(request))

	return HttpResponseRedirect('/')

def aboutAdmin(request):
	aboutData = About.objects.all()
	if request.POST.get('action') == 'about':
		countDat = About.objects.all().count()
		#save data if aboutData == 0
		name = request.POST.get('name')
		dob = request.POST.get('dob')
		pob = request.POST.get('pob')
		profession = request.POST.get('profession')
		interests = request.POST.get('interests')
		residence = request.POST.get('residence')
		phone = request.POST.get('phone')
		email = request.POST.get('email')
		website = request.POST.get('website')
		desc = request.POST.get('desc')
		idAbout = request.POST.get('idAbout')
		dAbout = About()

		dAbout.name = name
		dAbout.dob = dob
		dAbout.pob = pob
		dAbout.profession = profession
		dAbout.interests = interests
		dAbout.residence = residence
		dAbout.phone = phone
		dAbout.email = email
		dAbout.website = website
		dAbout.desc = desc
		dAbout.seqAbout = countDat

		dAbout.save()
		aboutData = About.objects.all()
		visibleAbout = aboutData.count()
		json_data = {'alert': 'Insert Data Success!!'}
		return HttpResponse(simplejson.dumps(json_data), content_type="application/json")

	return render_to_response('admin-panel/about.html', locals(), context_instance=RequestContext(request))
	#if request.user.is_authenticated():
	#	aboutDataData = About.objects.all()
	#	visibleAbout = aboutData.count()


	#return HttpResponseRedirect('/')

def logo(request):
	if request.POST.get('action') == 'logo':
		countDat = Logo.objects.all().count()
		#save data if logoData == 0
		name = request.POST.get('name')
		title = request.POST.get('title')
		dataId = request.POST.get('id')
		dLogo = Logo()
		if countDat != 0:
		    #condition for update data
		    if dataId != 'insert data':
		        dLogo = Logo.objects.get(seqLogo=int(dataId))
		        dLogo.nameLogo = name
		        dLogo.titleLogo = title
		        dLogo.seqLogo = int(dataId)
		        dLogo.save()
		        logoData = Logo.objects.all()
		        visibleTable = logoData.count()
		        json_data = {'alert': 'Update Data Success!!'}
		        return HttpResponse(simplejson.dumps(json_data), content_type="application/json")
		    logoData = Logo.objects.all()
		    visibleLogo = logoData.count()
		    json_data = {'alert': 'Sorry, data is only one!!'}
		    return HttpResponse(simplejson.dumps(json_data), content_type="application/json")

		dLogo.nameLogo = name
		dLogo.titleLogo = title
		dLogo.seqLogo = countDat
		dLogo.save()
		logoData = Logo.objects.all()
		visibleLogo = logoData.count()
		json_data = {'alert': 'Insert Data Success!!'}
		return HttpResponse(simplejson.dumps(json_data), content_type="application/json")

	elif request.POST.get('action') == 'delLogo':
		id = request.POST.get('id')
		delData = Logo.objects.filter(seqLogo=int(id))
		delData.delete()

		logoData = Logo.objects.all()
		visibleLogo = logoData.count()
		return render_to_response('admin-panel/logo_table.html', locals(), context_instance=RequestContext(request))

	if request.user.is_authenticated():
		logoData = Logo.objects.all()
		visibleLogo = logoData.count()
		return render_to_response('admin-panel/header.html', locals(), context_instance=RequestContext(request))

	return HttpResponseRedirect('/')

def skill(request):
	if request.POST.get('action') == 'skill':
		countDat = Skill.objects.all().count()
		#save data if skillData == 0
		varSkill = request.POST.get('skill')
		dataId = request.POST.get('id')
		try:
			dSkill = Skill.objects.get(seqSkill=int(dataId))
		except Exception, e:
			dSkill = Skill()
			dSkill.nameSkill = varSkill
			dSkill.seqSkill = countDat
			dSkill.save()
			skillData = Skill.objects.all()
			visibleSkill = skillData.count()
			json_data = {'alert': 'Insert Data Success!!'}
			return HttpResponse(simplejson.dumps(json_data), content_type="application/json")
		else:
			dSkill.nameSkill = varSkill
			dSkill.seqSkill = int(dataId)
			dSkill.save()
			skillData = Skill.objects.all()
			visibleSkill = skillData.count()
			json_data = {'alert': 'Update Data Success!!'}
			return HttpResponse(simplejson.dumps(json_data), content_type="application/json")

	elif request.POST.get('action') == 'delSkill':
		id = request.POST.get('id')
		delData = Skill.objects.filter(seqSkill=int(id))
		delData.delete()
		skillData = Skill.objects.all()
		visibleSkill = skillData.count()
		return render_to_response('admin-panel/skill_table.html', locals(), context_instance=RequestContext(request))

	if request.user.is_authenticated():
		skillData = Skill.objects.all()
		visibleSkill = skillData.count()
		return render_to_response('admin-panel/header.html', locals(), context_instance=RequestContext(request))

	return HttpResponseRedirect('/')

def services(request):
	if request.POST.get('action') == 'service':
		countDat = Service.objects.all().count()
		#save data if serviceData == 0
		varTitle = request.POST.get('title')
		varDesc = request.POST.get('desc')
		varIcon = request.POST.get('icon')
		dataId = request.POST.get('id')
		try:
			dService = Service.objects.get(seqService=int(dataId))
		except Exception, e:
			dService = Service()
			dService.title = varTitle
			dService.desc = varDesc
			dService.icon = varIcon
			dService.seqService = countDat
			dService.save()
			serviceData = Service.objects.all()
			visibleService = serviceData.count()
			json_data = {'alert': 'Insert Data Success!!'}
			return HttpResponse(simplejson.dumps(json_data), content_type="application/json")
		else:
			dService.title = varTitle
			dService.desc = varDesc
			dService.icon = varIcon
			dService.seqService = countDat
			dService.save()
			serviceData = Service.objects.all()
			visibleService = serviceData.count()
			json_data = {'alert': 'Update Data Success!!'}
			return HttpResponse(simplejson.dumps(json_data), content_type="application/json")

	if request.user.is_authenticated():
		serviceData = Service.objects.all()
		visibleService = serviceData.count()
		return render_to_response('admin-panel/services.html', locals(), context_instance=RequestContext(request))
	return render_to_response('admin-panel/services.html', locals(), context_instance=RequestContext(request))