# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from datetime import datetime


class Logo(models.Model):
	nameLogo = models.CharField(null=True, max_length=50)
	titleLogo = models.CharField(null=True, max_length=50)
	seqLogo = models.IntegerField(null=True)

	def __unicode__(self):
		return self.seqLogo

class SocMed(models.Model):
	link = models.CharField(null=True,max_length=50)
	icon = models.CharField(null=True,max_length=50)
	seqSoc = models.CharField(null=True,max_length=50)

	def __unicode__(self):
		return self.seqSoc


class About(models.Model):
	name = models.CharField(null=True, max_length=50)
	dob = models.DateField(null=True)
	pob = models.CharField(null=True, max_length=50)
	profession = models.CharField(null=True, max_length=50)
	interests = models.CharField(null=True, max_length=50)
	residence = models.CharField(null=True, max_length=50)
	phone = models.CharField(null=True, max_length=50)
	email = models.CharField(null=True, max_length=50)
	website = models.CharField(null=True, max_length=50)
	desc = models.CharField(null=True)
	seq_about = models.IntegerField(null=True)
	active = models.CharField(default='False')

	def __unicode__(self):
		return self.dob


class Skill(models.Model):
	nameSkill = models.CharField(null=True, max_length=50)
	seqSkill = models.IntegerField(null=True)

	def __unicode__(self):
		return self.nameSkill


class Service(models.Model):
	timestamp = models.DateTimeField(null=True)
	icon = models.CharField(null=True, max_length=100)
	title = models.CharField(null=True, max_length=100)
	desc = models.CharField(null=True, max_length=300)
	seqService = models.IntegerField(null=True)

	def __unicode__(self):
		return self.icon

