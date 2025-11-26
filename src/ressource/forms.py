from django import forms
from crum import get_current_user
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User, Group
from ressource.models.users import Profil
from workload.models import Implication

class ImplicationForm(forms.ModelForm):
    class Meta:
        model = Implication
        fields = ['nature', 'contribution', 'role']
        widgets = {
            'nature': forms.Select(attrs={'class': 'form-select'}),
            'contribution': forms.NumberInput(attrs={
                "type": "range", 
                "min": 0, 
                "max": 100, 
                "class": "form-range"}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
        }

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

		# Attribuer groupes + infos
		group = self.cleaned_data.get("groups")
		user.first_name = self.cleaned_data.get("first_name")
		user.last_name = self.cleaned_data.get("last_name")

		plain_password = self.cleaned_data.get("password1")
		user.set_password(plain_password)

		# Superadmin ?
		if group.name == "Superadmin":
			user.is_superuser = True

		user.save()
		user.groups.add(group)

		# Créer EmailAddress allauth
		from allauth.account.models import EmailAddress
		email_address = EmailAddress.objects.create(
			user=user,
			email=user.email.lower(),
			primary=True,
			verified=False,
		)

		# Envoyer email confirmation
		email_address.send_confirmation()

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

