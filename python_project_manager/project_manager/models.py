from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
	"""Class represents a project entity."""
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True, default='no description set')
	owner = models.CharField(blank=True, max_length=32, default='root')
	
	def __unicode__(self):
		return self.title

class UserProfile(models.Model):
	"""Class is an extension of standart user with an icon."""
	user = models.OneToOneField(User)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __unicode__(self):
		return self.user.username

class UserRole(models.Model):
	"""Class represents user roles in projects."""
	user = models.ForeignKey(User)
	project = models.ForeignKey(Project)
	role = models.CharField(max_length=32)

	def __unicode__(self):
		return self.role

class TaskGroup(models.Model):
	"""Represents groups of tasks"""
	name = models.CharField(max_length=200)
	roles = models.CharField(max_length=200)
	project = models.ForeignKey(Project)

	def __unicode__(self):
		return self.name

""" [ Task 16 """
class TaskName(models.Model):
	task_Name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.task_Name

class TaskDescription(models.Model):
	task_Description = models.CharField(max_length=1000)

	def __unicode__(self):
		return self.task_Description

class Employer(models.Model):
	employer = models.CharField(max_length=50)

	def __unicode__(self):
		return self.employer

class Developer(models.Model):
	Developer = models.CharField(max_length=50)

	def __unicode__(self):
		return self.Developer

class TaskPriority(models.Model):
	task_Priority = models.IntegerField(default=0)
""" ] """

