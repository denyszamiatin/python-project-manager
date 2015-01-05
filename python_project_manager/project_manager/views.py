import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _

from project_manager.forms import *
from includes.common import *

from django.shortcuts import render
from django_ajax.decorators import ajax
from project_manager.models import TaskGroup


@login_required()
def home(request):
	"""Represents user's projects in which he is involved"""
	context = RequestContext(request)
	projects = Project.objects.all().filter(owner=request.user.username)

	return render_to_response('login/login_template.html', {'projects': projects}, context)


@login_required()
def main_page(request):
	"""Represents some user profile data and user abilities."""
	context = RequestContext(request)
	projects = UserRole.objects.all().filter(user=request.user)
	return render_to_response('main/main_template.html', {'projects': projects}, context)


@login_required()
def project(request, project_id="0"):
	context = RequestContext(request)
	project = Project.objects.filter(id=project_id)[0]
	projects = UserRole.objects.all().filter(user=request.user)
	menu = pm_menu('project', request, {'project': project})
	return render_to_response('project_model/project_page_template.html',
							  {'current_project': project, 'projects': projects, 'menu': menu}, context)


@login_required()
def project_settings(request, id="0"):
    context = RequestContext(request)
    project = Project.objects.filter(id = id)[0]
    projects = UserRole.objects.all().filter(user = request.user)

    if project.owner != request.user.username:
        messages.error(request, "You don't have a permission to view this project!")

        return HttpResponseRedirect('/main/')

    if request.method == 'POST':
        project_form = ProjectForm(data=request.POST)
        if project_form.is_valid():
            updated_project = project_form.instance
            updated_project.id = id
            updated_project.save()

            messages.info(request, "Project settings updated!")
            return HttpResponseRedirect('/main/')
        else:
            messages.error(request, "Failed to save project settings!")
    else:
        project_form = ProjectForm(instance = project)

    return render_to_response('project_model/project_settings_template.html',
                              {'current_project': project,
                               'projects': projects,
                               'project_form': project_form}, context)


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
def project_create(request):
	"""Represents a page for project creation."""
	context = RequestContext(request)

	if request.method == 'POST':
		project_form = ProjectForm(data=request.POST)
		if project_form.is_valid():
			project = project_form.save()
			project.owner = request.user.username
			project.save()

			user_role = UserRole(user=request.user, role='owner', project=project)
			user_role.save()


			default_task_group = TaskGroup(name='Default group', project=project)
			default_task_group.save()

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


def add_user_to_project(request, project_id="0"):
	"""Represents a page for project member administration."""
	if request.method == 'POST':
		user_id = request.POST.get('id')
		value = request.POST.get('value')
		role_to_update = None
		try:
			role_to_update = UserRole.objects.get(user_id = user_id, project_id= project_id)
		except:
			print 'failed'

		if not role_to_update:
			project = Project.objects.get(id = project_id)
			user = User.objects.get(id = user_id)
			new_role = UserRole()
			new_role.project = project
			new_role.user = user
			new_role.role = value
			new_role.save()
			role_to_update = new_role
		else:
			role_to_update.role = value
			role_to_update.save()
		role_names = {'none': _('None'), 'owner': _('Owner'), 'admin': _('Administrator'), 'performer': _('Performer')}
		response_data = {'user_id': role_to_update.user.id, 'role': role_to_update.role, 'role_names': role_names}

		return HttpResponse(
			json.dumps(response_data),
			content_type="application/json"
        )
	else:
		context = RequestContext(request)
		users = User.objects.all()
		roles = [
			('none', _('None')),
			('owner', _('Owner')),
			('admin', _('Administrator')),
			('performer', _('Performer')),
		]
		data = []
		for user in users:
			user_role = UserRole.objects.filter(user=user, project_id=project_id).first()
			data.append({
				'user': user,
				'role': user_role,
				'form': EditRoleForm({'choices': roles})
			})
		return render_to_response('project_model/users.html', {'data': data}, context)


@ajax
def get_task_groups(request, id="0"):
    task_groups = TaskGroup.objects.filter(project = id).prefetch_related('tasks')

    return render(request, 'partials/task_group_template.html', {
        'task_groups' : task_groups
    })
