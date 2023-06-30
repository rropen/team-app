"""
URL configuration for teams_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
import teams_app.views as views
from teams_app.api_router import api_router

urlpatterns = [
    path('', views.home_page_view, name="home_page"),
    path('login', views.login_page_view, name="login_page"),
    path('signup', views.signup_page_view, name="register"),
    path('team_viewer', views.team_viewer_view, name="team_viewer"),
    path('team_management', views.team_management_view, name="team_management"),
    path('create_team', views.create_team_view, name="create_team"),
    path('documentation', views.documentation_view, name="documentation"),
    path('team/<int:team_id>', views.focus_team_view, name="focus_team"),
    path('profile', views.profile, name="profile"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path("api/", include(api_router.urls)),
    re_path(r"^users_teams/(?P<username>)$", include(api_router.urls))
]