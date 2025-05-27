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
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Use ModelChoiceField to ensure the form returns a Member instance as per the login user
        if user.is_staff:
            self.fields["account"] = forms.ModelChoiceField(
                queryset=Member.objects.all(),
                widget=forms.Select(attrs={"class": "form-control"}),
                required=True,
                )
        elif user.managed_community.exists(): # Checks and filter the Member base on Community Head
            communities = user.managed_community.all()
            self.fields["account"] = forms.ModelChoiceField(
                queryset=Member.objects.filter(community__in=communities),
                widget=forms.Select(attrs={"class": "form-control"}),
                required=True,
                )
        else: # Not necessary Code and Normal Member Can't Access This Form
            self.fields["account"] = forms.ModelChoiceField(
                queryset=Member.objects.none(),
                widget=forms.Select(attrs={"class": "form-control"}),
                required=True,
                )
        
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

        
