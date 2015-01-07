from django.template import Context, loader
from array import *
from django.utils.translation import ugettext as _
from project_manager.models import Project, UserRole
import inspect

def pm_render(*args, **kwargs):
	t = loader.get_template('test.html')
	c = Context({})
	rendered = loader.render_to_string(*args, **kwargs)
	return rendered

def pm_menu(menu_name = '', request = '', args={}):
	if menu_name == '':
		return ''
	menus = {
		"project" : pm_project_menu
	}
	items = menus[menu_name](request, args)
	output = loader.render_to_string("partials/menu.html", {'menu':items})
	return output

def pm_main_menu(request = '', agrs={}):
	items = [
		{
			'title': _('Project'),
			'href': '#',
			'sub_menu': [{'title': _('Create project'), 'href': '/new_project'},]
		}
	]
	return items

def pm_project_menu(request='', args={}):
	current_project = args['project']
	projects = UserRole.objects.all().filter(user=request.user)
	items = pm_main_menu(request)
	items[0]['sub_menu'].append({'title': _('Add user to project'), 'href': '/test'})
	items.append({
		'title':_('Settings'),
		'href': '#',
		'sub_menu': [{'title': _('Add user to project'), 'href': '/project/' + str(current_project.id) + '/add-user'},
                     {'title': _('Change settings'), 'href': '/project/' + str(current_project.id) + '/settings'}]
	})
	return items

