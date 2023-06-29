from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Team, Relationship

from difflib import SequenceMatcher

#JC - Form for the user to login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

#JC - Form for the user to register
class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username', 'email', 'password1', 'password2']

#JC - Form to add a team to the database using the Team model
class CreateTeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ["name", "description", "private"]
    
    #JC - Requirements for the team name
    name = forms.CharField(
        min_length=3,
        max_length=64,
        required=True
    )

    #JC - Description field
    description = forms.CharField(
        max_length=512,
        required=False
    )

    #JC - Private field
    private = forms.BooleanField(
        required=False
    )

    def clean(self):
        cleaned_data = super(CreateTeamForm, self).clean()
        team_name = cleaned_data.get('name')
        teams = Team.objects.all()
        error_set = False
        for team in teams:
            similarity = SequenceMatcher(None, team_name, team.name).ratio()
            if similarity >= 0.9 and not error_set:
                self.add_error('name', 'This name is to similar to an existing team name.')
                error_set = True
        return cleaned_data
