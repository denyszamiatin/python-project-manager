from project_manager.models import UserProfile, Project
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from django.utils.translation import ugettext as _

class UserForm(forms.ModelForm):
	"""Form for standart user registration."""
	error_messages = {
		'password_mismatch': _("The two password fields didn't match."),
	}
	username = forms.CharField(help_text=_("Please enter a username."))
	first_name = forms.CharField(help_text=_("Please enter a firstname."))
	last_name = forms.CharField(help_text=_("Please enter a lastname."))
	email = forms.CharField(help_text=_("Please enter your email."))
	password1 = forms.CharField(widget=forms.PasswordInput(), help_text=_("Please enter a password."))
	password2 = forms.CharField(widget=forms.PasswordInput(), 
								help_text=_("Please enter a password again."))
	
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name',
				  'email', 'password1', 'password2')
	
	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(
				self.error_messages['password_mismatch'],
				code='password_mismatch',
			)
		return password2

class UserProfileForm(forms.ModelForm):
	"""Form for additional user data."""
	class Meta:
		model = UserProfile
		fields = ('picture',)

class ProjectForm(forms.ModelForm):
	"""Form for creating a project."""
	title = forms.CharField(label=_("Project title"))
	description = forms.CharField(widget=forms.Textarea, label=_("Project description"), required=False)
	owner = forms.CharField(widget=forms.HiddenInput(), required=False)
	
	class Meta:
		model = Project
		fields = ('title', 'description', 'owner')