from teams_app.models import User, UserToken, Role
from django.http.request import HttpRequest
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
import hashlib

def teams_permission_check(request:HttpRequest, username):
    token = request.META.get("HTTP_TEAMS_TOKEN")
    if not token:
        raise AuthenticationFailed("No Token Found")
    expected_token = hashlib.sha256((username + "AbsencePlanner").encode()).hexdigest()
    if expected_token != token:
        raise PermissionDenied("Invalid Token")

def verify_user_token(request:HttpRequest):
    """
    Takes the user's token from the request headers and matches it against a user's token in the
    Team App database. This is the hash of the user's username, which should be the same between
    both the Team App and the app querying the API (e.g., the Absence Planner). Returns a valid
    username.

    This might seem insecure at first as validating the users identity through a simple request
    header can be easily forged. However, this is a private API that requires the use of an API
    key, and the querying app (i.e., the Absence Planner) pulls the username from the user's
    session and sends it to this private API, so the API request can be trusted.
    """

    try:
        given_username_hash = request.headers["User-Token"]
        user_token = UserToken.objects.get(username_hash=given_username_hash)
    except:
        raise AuthenticationFailed("No User Token Found")

    stored_username_hash = user_token.username_hash
    if (given_username_hash != stored_username_hash):
        raise PermissionDenied("Invalid User Token")

    user = User.objects.get(id=user_token.user_id)

    return user.username
