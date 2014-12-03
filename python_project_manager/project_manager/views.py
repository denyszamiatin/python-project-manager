import os.path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from project_manager.models import Project, User, UserProfile
from project_manager.forms import ProjectForm, UserForm, UserProfileForm

@login_required()
def main_page(request):
	"""Represents some user profile data and user abilities."""
	context = RequestContext(request)
	return render_to_response('main/main_template.html', {}, context)

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
def project_create(request):
	"""Represents a page for project creation."""
	context = RequestContext(request)

	if request.method == 'POST':
		project_form = ProjectForm(data=request.POST)
		
		if project_form.is_valid():
			project = project_form.save()
			project.owner = request.user.username
			project.save()
			
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