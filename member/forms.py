from dataclasses import fields
from django import forms
from .models import *


class MemberCreationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = "__all__"

        exclude = ['age', 'member_id']

        widgets = {
            "dob": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class CommunityCreationForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})