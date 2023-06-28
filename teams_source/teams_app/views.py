from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from .forms import LoginForm, RegisterForm, CreateTeamForm
from .models import Team, Role, Relationship

import json

#JC - Home page view
def home_page_view(request):
    return render(request, "pages/home_page.html", {"home_active": True})

#JC - Login page view
def login_page_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                return render(request, "pages/login_page.html", {"form": form, "message": "Invalid Username or Password"})
        else:
            print(form.errors)
    else:
        form = LoginForm()
    return render(request, "pages/login_page.html", {"form": form})

#JC - Sign up page view
def signup_page_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            login(request, user)
            return redirect("/")

    else:
        form = RegisterForm()
    return render(request, "pages/sign_up_page.html", {"form": form})

#JC - Team viewer page
@login_required
def team_viewer_view(request):

    if request.method == "POST":
        data = json.loads(request.body)
        if data["type"] == "remove":
            rel = Relationship.objects.filter(user=request.user, team_id=data["team_id"])
            rel.delete()
        elif data["type"] == "add":
            rel = Relationship.objects.create(
                user=request.user,
                team=Team.objects.get(id=data["team_id"]),
                role=Role.objects.get(role="Member")
            )
            rel.save()

    relationships = Relationship.objects.order_by(Lower("role__id")).filter(user=request.user)
    all_teams = Team.objects.all().order_by(Lower("name")).exclude(relationship__user=request.user.id)
    teams_data = {
        "relationships": relationships,
        "teams_amount": len(relationships),
        "public_teams": all_teams,
        "public_team_amount": len(all_teams)
    }

    return render(request, "pages/teams/team_viewer.html", {"viewer_active": True, **teams_data})

@login_required
def focus_team_view(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
    except:
        return redirect("/team_viewer")
    return render(request, "pages/teams/focus_team.html", {"team": team})

#JC - Team management page
@login_required
def team_management_view(request):
    return render(request, "pages/teams/team_manager.html", {"management_active": True})

#JC - Create team view
@login_required
def create_team_view(request):
    if request.method == "POST":
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            form.save()
            #JC - Creates relationship between user and team
            created_team = Team.objects.get(name=form.cleaned_data["name"])
            assign_role = Role.objects.get(role="Owner")
            Relationship.objects.create(
                user = request.user,
                team = created_team,
                role = assign_role
            )
            return redirect("/")
    else:
        form = CreateTeamForm()
    return render(request, "pages/teams/create_team.html", {"creation_active": True, "form": form})

#JC - Documentation page view
@login_required
def documentation_view(request):
    return render(request, "pages/documentation.html", {"documentation_active": True})