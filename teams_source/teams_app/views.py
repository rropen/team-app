from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from .forms import LoginForm, RegisterForm, CreateTeamForm
from .models import Team, Role, Relationship, Status, UserProfile
import holidays, pycountry
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
        #JC - Leave a team
        if data["type"] == "remove":
            rel = Relationship.objects.filter(user=request.user, team_id=data["team_id"])
            rel.delete()
        #JC - Join a team
        elif data["type"] == "add":
            rel = Relationship.objects.create(
                user=request.user,
                team=Team.objects.get(id=data["team_id"]),
                role=Role.objects.get(role="Member"),
                status=Status.objects.get(id=1)
            )
            rel.save()
        elif data["type"] == "accept":
            rel = Relationship.objects.filter(user=request.user, team_id=data["team_id"])[0]
            rel.status = Status.objects.get(id=1)
            rel.save()
        elif data["type"] == "decline":
            rel = Relationship.objects.filter(user=request.user, team_id=data["team_id"])
            rel.delete()

    relationships = Relationship.objects.order_by(Lower("role__id")).filter(user=request.user, status=1)
    all_teams = Team.objects.all().order_by(Lower("name")).exclude(relationship__user=request.user.id).exclude(private=True)
    invite_list = Relationship.objects.filter(status=2)
    teams_data = {
        "relationships": relationships,
        "teams_amount": len(relationships),
        "public_teams": all_teams,
        "public_team_amount": len(all_teams),
        "invite_list": invite_list,
        "invite_amount": len(invite_list)
    }

    return render(request, "pages/teams/team_viewer.html", {"viewer_active": True, **teams_data})

#JC - The view for the individual team view
@login_required
def focus_team_view(request, team_id):

    #JC - This will redirect them if they don't have permission to view the team
    if Team.objects.filter(id=team_id)[0].private:
        if not Relationship.objects.filter(user=request.user, team_id=team_id, status=1).exists():
            return redirect("/team_viewer")

    #JC - This recives the data from the web page
    messages = []
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except:
            data = None
        if data != None:
            if data["type"] == "remove":
                rel = Relationship.objects.filter(user_id=data["user_id"], team_id=team_id)
                rel.delete()
            elif data["type"] == "delete_team":
                print("Deleting team")
                Team.objects.get(id=team_id).delete()
                return redirect("/team_viewer")
        else:
            if "name" in request.POST and "description" in request.POST:
                team_edit_form = CreateTeamForm(request.POST)
                current_team = Team.objects.get(id=team_id)
                current_team.name = team_edit_form.data["name"]
                current_team.description = team_edit_form.data["description"]
                if team_edit_form.data["private"] == "on":
                    current_team.private = True
                else:
                    current_team.private = False
                current_team.save()
            elif "user" in request.POST and "role" in request.POST:
                if request.POST.get("user"):
                    user = User.objects.filter(username=request.POST.get("user"))
                    if user.exists():
                        rel = Relationship.objects.create(
                            user=user[0],
                            team=Team.objects.get(id=team_id),
                            role=Role.objects.get(role=request.POST.get("role")),
                            status=Status.objects.get(id=2)
                        )
                        rel.save()
                    else:
                        messages.append("Username not found.")
                else:
                    messages.append("A username is required.")
    
    team_form_data = {
        "name": Team.objects.get(id=team_id).name,
        "description": Team.objects.get(id=team_id).description,
        "private": Team.objects.get(id=team_id).private
    }
    
    team_edit_form = CreateTeamForm(team_form_data)

    try:
        team = Team.objects.get(id=team_id)
    except:
        return redirect("/team_viewer")
    
    member_list = Relationship.objects.filter(team=team, status=1)
    role_list = Role.objects.all()
    user_permission = False
    if Relationship.objects.filter(team=team_id, status=1, role=1, user=request.user).exists():
        user_permission = True
    elif Relationship.objects.filter(team=team_id, status=1, role=2, user=request.user).exists():
        user_permission = True
    
    if Relationship.objects.filter(user=request.user, status=1, team_id=team_id).exists():
        user_role_id = Relationship.objects.filter(user=request.user, status=1, team_id=team_id)[0].role.id
    else:
        user_role_id = 10

    return render(request, "pages/teams/focus_team.html", {"team": team, "team_members": member_list, "roles": role_list, 
                    "user_permission": user_permission, "role_id": user_role_id, "team_id": team_id, "messages": messages, "edit_form": team_edit_form})

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
            Relationship.objects.create(
                user = request.user,
                team = Team.objects.get(name=form.cleaned_data["name"]),
                role = Role.objects.get(role="Owner"),
                status = Status.objects.get(id=1)
            )
            return redirect("/")
    else:
        form = CreateTeamForm()
    return render(request, "pages/teams/create_team.html", {"creation_active": True, "form": form})

#JC - Documentation page view
@login_required
def documentation_view(request):
    return render(request, "pages/documentation.html", {"documentation_active": True})

def profile(request):

    userprofile: UserProfile = UserProfile.objects.filter(user=request.user)

    if not userprofile.exists():
        userprofile = UserProfile.objects.create(
            user=request.user,
            accepted_policy=True,
            region="GB"
        )
        userprofile.save()
    else:
        userprofile: UserProfile = UserProfile.objects.get(user=request.user)


    if request.method=="POST" and len(request.POST) > 0:
        if request.POST.get("firstName") != "" and request.POST.get("firstName") != request.user.first_name:
            request.user.first_name = request.POST.get("firstName")
            request.user.save()
        if request.POST.get("lastName") != "" and request.POST.get("lastName") != request.user.last_name:
            request.user.last_name = request.POST.get("lastName")
            request.user.save()
        if request.POST.get("email") != request.user.email:
            request.user.email = request.POST.get("email")
            request.user.save()        

        region = request.POST.get("region")
        region_code = pycountry.countries.get(name=region).alpha_2

        

        if region_code != userprofile.region:
            userprofile.region = region_code
            userprofile.save()

    countries = []
    for country in list(pycountry.countries):
        try:
            holidays.country_holidays(country.alpha_2)
            countries.append(country.name)
        except:
            pass
    
    countries = sorted(countries)

    country_name = pycountry.countries.get(alpha_2=userprofile.region).name

    context = {"countries":countries, "current_country":country_name}
    return render(request, "pages/profile.html", context)