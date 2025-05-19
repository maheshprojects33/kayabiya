from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    SetPasswordForm,
    PasswordChangeForm,
    UserChangeForm,
)
from django.contrib.auth.models import User



class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "e.g. lakasa.nepal"}
        )
        self.fields["first_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "e.g. Lakasa"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "e.g. Nepal"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "e.g. info@lakasanepal.org"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "readonly": "readonly"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "readonly": "readonly"}
        )

        # Set default password of new user
        self.fields["password1"].widget.attrs.update({"value": "KayaBiya@1"})
        self.fields["password2"].widget.attrs.update({"value": "KayaBiya@1"})

        # Set fields as required
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True


# For For Admins Only to Reset User's Password
class UserPasswordResetForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs.update(
            {"placeholder": "New Password", "class": "form-control"}
        )
        self.fields["new_password2"].widget.attrs.update(
            {"placeholder": "Confrim Password", "class": "form-control"}
        )


# For Users To Change Their Own Password
class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Old Password"}
        ),
    )
    new_password1 = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "New Password"}
        ),
    )
    new_password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        ),
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["first_name"].widget.attrs.update({"class": "form-control"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control"})


class LoginForm(forms.ModelForm):
    username = forms.CharField(
        max_length=254, widget=forms.TextInput(attrs={"class": "form-control p_input"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control p_input"}),
        label="Password",
    )

    class Meta:
        model = User
        fields = ("username", "password")
