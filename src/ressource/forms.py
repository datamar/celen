from django import forms
from crum import get_current_user
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User, Group
from ressource.models.users import Profil

class ImportUserForm(forms.Form):
    fichier = forms.FileField(label="Fichier CSV")

class CustomUserCreateForm(UserCreationForm):
	groups = forms.ModelChoiceField(
		queryset=Group.objects.all(),
		widget=forms.RadioSelect(attrs={'class': "form-check-input"}),
		required=True)

	class Meta:
		model = User
		fields = ["username","last_name","first_name","groups","email"]
		widgets = {'groups':forms.RadioSelect(attrs={'class':"form-check-input"})}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		current_user = get_current_user()
		if not current_user.is_superuser:
			self.fields["groups"].queryset = Group.objects.exclude(name="Superadmin")
		else:
			self.fields["groups"].queryset = Group.objects.all()
		if current_user.groups.filter(name="Gestionnaire").exists():
			self.fields["groups"].queryset = Group.objects.exclude(name__in=["Superadmin","Administrateur"])

	def save(self, commit=True):
		"""
		Sauvegarde l'utilisateur et lui assigne le groupe sélectionné.
		"""
		user = super().save(commit=False)
		current_user = get_current_user()
		# Ajouter le groupe sélectionné à l'utilisateur
		group = self.cleaned_data.get('groups')
		if group == "Superadmin":
			user.is_superuser = True
		plain_password = self.cleaned_data.get('password1')
		print ("mot de passe: "+plain_password)
		user._plain_password = plain_password
		user.save()  # Sauvegarder l'utilisateur pour qu'il ait un ID
		user.groups.add(group)
		user.profile.prenom = self.cleaned_data.get("first_name")
		user.profile.nom_de_famille = self.cleaned_data.get('last_name')
		user.profile.save()
		return user

class UserUpdateForm(UserChangeForm):
	class Meta:
		model = User
		fields = ['username','email','first_name','last_name']
		#widgets = {'groups':forms.CheckboxSelectMultiple(attrs={'class':"form-check-input"})}

class ProfileUpdateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ProfileUpdateForm, self).__init__(*args, **kwargs)
		instance = kwargs.get('instance')
		if instance:
			#self.fields['roles'].queryset = instance.roles.all()
			#self.fields["roles"].label = False
			self.fields["photo"].label = "Avatar"

	class Meta:
		model = Profil
		fields = ['photo','bio',"phone"]

