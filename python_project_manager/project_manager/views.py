import os.path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from project_manager.models import Project, User, UserProfile, UserRole
from project_manager.forms import ProjectForm, UserForm, UserProfileForm

@login_required()
def home(request):
	"""Represents user's projects in which he is involved"""
	context = RequestContext(request)
	projects = Project.objects.all().filter(owner = request.user.username)

	return render_to_response('login/login_template.html', {'projects': projects}, context)

@login_required()
def main_page(request):
	"""Represents some user profile data and user abilities."""
	context = RequestContext(request)
	projects = UserRole.objects.all().filter(user = request.user)
	return render_to_response('main/main_template.html', {'projects': projects}, context)

def user_login(request):
	"""Represents a user login page."""
	context = RequestContext(request)

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				messages.success(request, "Login Successful!")
				return HttpResponseRedirect('/main/')
			else:
				messages.error(request, "You are banned!")
				return render_to_response('login/login_template.html', 
										 {}, context)
		else:
			print "Invalid login details: {0}, {1}".format(username, 
														   password)
			messages.error(request, "Invalid login details!")
			return render_to_response('login/login_template.html', 
									 {}, context)
	else:
		return render_to_response('login/login_template.html', 
								  {}, context)

@login_required()
def user_logout(request):
	context = RequestContext(request)
	logout(request)
	return redirect('/')

@login_required()
def project_page_open(request):
	context = RequestContext(request)
	project = Project.objects.filter(id=request.GET['id'])[0]

	return render_to_response('project_page/project_page_template.html',
								  {'project': project}, context)


@login_required()
def project_create(request):
	"""Represents a page for project creation."""
	context = RequestContext(request)

	if request.method == 'POST':
		project_form = ProjectForm(data=request.POST)
		if project_form.is_valid():
			project = project_form.save()
			project.owner = request.user.username
			project.save()

			user_role = UserRole(user = request.user, role = 'owner', project = project)
			user_role.save()

			messages.info(request, "Project created!")
			return HttpResponseRedirect('/main/')
		else:
			messages.error(request, "Failed to create a project!")
		
	else:
		project_form = ProjectForm()
	
	return render_to_response('project_model/project_template.html', 
							 {'project_form': project_form}, context); 

def register(request):
	"""Represents a page for user registration."""
	context = RequestContext(request)

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
		
			user = user_form.save()
			user.set_password(user_form.cleaned_data["password1"])
			user.save()
			
			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()
			messages.success(request, "Registration successful!")
			return HttpResponseRedirect('/login/')
		else:
			print user_form.errors, profile_form.errors
			messages.error(request, "Registration failed!")

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render_to_response(
			'registration/registration_template.html',
			{'user_form': user_form, 'profile_form': profile_form},
			context)	