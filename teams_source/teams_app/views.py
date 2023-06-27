from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm, CreateTeamForm

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
def team_viewer_view(request):
    return render(request, "pages/teams/team_viewer.html", {"viewer_active": True})

#JC - Team management page
def team_management_view(request):
    return render(request, "pages/teams/team_manager.html", {"management_active": True})

#JC - Create team view
def create_team_view(request):
    if request.method == "POST":
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = CreateTeamForm()
    return render(request, "pages/teams/create_team.html", {"creation_active": True, "form": form})

#JC - Documentation page view
def documentation_view(request):
    return render(request, "pages/documentation.html", {"documentation_active": True})