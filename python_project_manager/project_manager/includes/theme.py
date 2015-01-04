import importlib

def theme(hook, variables = {}):
	hooks = {
		"select" : theme_select
	}
	output = ''
	if hook != '':
		output = hooks[hook](variables)
	return output

def theme_select(variables = {}):
	output = ''
	return output
