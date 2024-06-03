from django import forms

class UserForm(forms.Form):
    team_id = forms.IntegerField()
