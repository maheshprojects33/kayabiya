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
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["role"].widget.attrs.update({"class": "form-control"})
        self.fields["community"].widget.attrs.update({"class": "form-control"})
        self.fields["membership_id"].widget.attrs.update({"class": "form-control"})
        self.fields["grand_parent"].widget.attrs.update({"class": "form-control"})
        self.fields["parent"].widget.attrs.update({"class": "form-control"})
        self.fields["spouse"].widget.attrs.update({"class": "form-control"})
        self.fields["gender"].widget.attrs.update({"class": "form-control"})
        self.fields["marital_status"].widget.attrs.update({"class": "form-control"})
        self.fields["mobile"].widget.attrs.update({"class": "form-control"})
        self.fields["address"].widget.attrs.update({"class": "form-control"})
        self.fields["ward"].widget.attrs.update({"class": "form-control"})
        self.fields["house_number"].widget.attrs.update({"class": "form-control"})
        self.fields["citizenship_number"].widget.attrs.update({"class": "form-control"})
        self.fields["join_date"].widget.attrs.update({"class": "form-control"})
        self.fields["profile_picture"].widget.attrs.update({"class": "form-control"})
        self.fields["citizen_copy"].widget.attrs.update({"class": "form-control"})
        self.fields["status"].widget.attrs.update({"class": "form-control"})


class CommunityCreationForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["community_name"].widget.attrs.update({"class": "form-control"})
        self.fields["community_head"].widget.attrs.update({"class": "form-control"})