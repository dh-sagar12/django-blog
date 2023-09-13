# from django import forms
from importlib.metadata import requires
from pkg_resources import require
from .models import User
from django.utils.translation import gettext_lazy as _
from django import forms as f



class UserCreationForm(f.ModelForm):
    def __init__(self, *args, **kwargs):
            super(UserCreationForm, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'block w-full px-4 py-2 mt-2 text-purple-600 bg-white border rounded-md focus:border-purple-400 focus:ring-purple-300 focus:outline-none focus:ring focus:ring-opacity-40'
    
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = f.CharField(label=_("Password"),
        widget=f.PasswordInput)
    password2 = f.CharField(label=_("Confirm Password"),
        widget=f.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))
    date_of_birth = f.DateField(widget=f.DateInput({'type': 'date'}), required=True)
    class Meta:
        model = User
        fields = ("email","first_name", "middle_name", "last_name", "date_of_birth", 'gender')
        widgets= {
            'email': f.EmailInput(attrs= {'placeholder': 'Enter your valid email address', }),
            'first_name': f.TextInput(attrs= {'placeholder': 'First Name'}),
            'middle_name': f.TextInput(attrs= {'placeholder': 'Middle Name'}),
            'last_name': f.TextInput(attrs= {'placeholder': 'Last Name'}),
            'password1': f.PasswordInput(attrs={'placeholder': 'Choose a password'}),
            'password2': f.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        }
        required_fields=(
            "date_of_birth",
            "gender"
        )
        error_messages = {
            'email': {
                'unique': _("User already exists!")
            },
            'date_of_birth': {
                'required': _('required')
            }
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise f.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EditProfileForm(f.ModelForm):
    def __init__(self, *args, **kwargs):
            super(EditProfileForm, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'block w-full px-4 py-2 mt-2 text-purple-600 bg-white border rounded-md focus:border-purple-400 focus:ring-purple-300 focus:outline-none focus:ring focus:ring-opacity-40'
            
            self.fields['avatar'].widget = f.FileInput(attrs={'accept': 'image/*'})

    date_of_birth = f.DateField(widget=f.DateInput({'type': 'date'}), required=True)
     
    class Meta:
        model  =  User
        fields  =  ('avatar', 'email', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender')
          