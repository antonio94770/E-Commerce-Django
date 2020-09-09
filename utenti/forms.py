from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
	username = forms.RegexField(regex=r'^[\w.@+-]+$', max_length=30, label="Username", error_messages={'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
	email = forms.EmailField(max_length=254)
	password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
	password2 = forms.CharField(widget=forms.PasswordInput, label="Password (reinserisci)")
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Formato numero di telefono: '+999999999', con un massimo di 15 cifre.")
	phone_number = forms.CharField(validators=[phone_regex], max_length=17, label="N.telefono")
	temporizzazione_giorni = forms.IntegerField(initial=0, min_value=0)
	
	
	
	def clean_username(self):
		existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
		if existing.exists():
			raise forms.ValidationError("L'username già esiste.")
		else:
			return self.cleaned_data['username']
			
	def clean_email(self):
		username = self.cleaned_data.get('username')
		email = self.cleaned_data.get('email')

		if email and User.objects.filter(email=email).exclude(username=username).count():
			raise forms.ValidationError('Email gia in uso.')
		return email

	def clean(self):
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError("Le due nuove password non combaciano.")
		return self.cleaned_data
		
		
class EditProfileForm(forms.ModelForm):

	username = forms.RegexField(regex=r'^[\w.@+-]+$', max_length=30, label="Username", error_messages={'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
	email = forms.EmailField(max_length=254)
	old_password = forms.CharField(widget=forms.PasswordInput, label="Vecchia password")
	new_password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
	new_password2 = forms.CharField(widget=forms.PasswordInput, label="Password (reinserisci)")
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Formato numero di telefono: '+999999999', con un massimo di 15 cifre.")
	phone_number = forms.CharField(validators=[phone_regex], max_length=17, label="N.telefono")
	temporizzazione_giorni = forms.IntegerField(min_value=0)

	
	class Meta:
		model = User
		fields = ['username', 'email', 'phone_number', 'old_password', 'new_password1', 'new_password2']

	
	def clean_username(self):
		if User.objects.filter(username__iexact=self.cleaned_data['username']).exclude(username = self.instance.username).count():
			raise forms.ValidationError("L'username già esiste.")
		else:
			return self.cleaned_data['username']
			
	def clean_email(self):
		username = self.cleaned_data['username']
		email = self.cleaned_data['email']

		if email and User.objects.filter(email=email).exclude(username=self.instance.username).count():
			raise forms.ValidationError('Email gia in uso.')
		return email

		
	def clean_old_password(self):
		old_password = self.cleaned_data['old_password']

		if not self.instance.check_password(old_password):
			raise forms.ValidationError('La vecchia password è errata.')

		return old_password

	def clean(self):
		if 'new_password1' in self.cleaned_data and 'new_password2' in self.cleaned_data:
			if self.cleaned_data['new_password1'] != self.cleaned_data['new_password2']:
				raise forms.ValidationError("Le due nuove password non combaciano.")
		return self.cleaned_data
		

class VoteForm(forms.Form):
	CHOICES=[(1,'Insufficiente'),
			(2,'Discreto'),
			(3, 'Buono'),
			(4, 'Ottimo'),
			(5, 'Eccellente')]

	voto = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())