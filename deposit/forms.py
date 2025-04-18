from django import forms
from .models import *
from django.forms import modelformset_factory


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = "__all__"

        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Use ModelChoiceField to ensure the form returns a Member instance
        self.fields["account"] = forms.ModelChoiceField(
            queryset=Member.objects.all(),
            widget=forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Select or enter account",
                    "list": "usernames-datalist",
                }
            ),
            required=True,
        )
        self.fields["account"].widget.attrs.update({"class": "form-control"})
        self.fields["deposit_amount"].widget.attrs.update({"class": "form-control"})
        self.fields["deposit_by"].widget.attrs.update({"class": "form-control"})
        self.fields["remarks"].widget.attrs.update({"class": "form-control"})

        # Store datalist HTML to render in the template
        members = Member.objects.all()
        self.datalist = "".join(
            [
                f'<option value="{member.id}">{member.username.get_full_name()} ({member.username})</option>'
                for member in members
            ]
        )
