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
	role = models.CharField(blank=True, max_length=32, default='owner')

	def __unicode__(self):
		return self.role

