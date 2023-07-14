from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.middleware.csrf import get_token


@login_required(login_url='/login/oidc/')
def logout_view(request):
    """
    Logs out the user.
        Args:
            request (HttpRequest): The request object.
        Returns:
            JsonResponse: A JSON response containing a message.
    """
    logout(request)
    return JsonResponse({'message': 'Logout successful'})


@login_required(login_url='/login/oidc/')
def csrf_token_view(request):
    """
    Returns a CSRF token.
        Args:
            request (HttpRequest): The request object.
        Returns:
            JsonResponse: A JSON response containing a CSRF token.
    """
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})


def check_login_status(request):
    """
    Checks if the user is logged in.
        Args:
            request (HttpRequest): The request object.
        Returns:
            JsonResponse: A JSON response containing a boolean indicating if the user is logged in.
    """
    is_logged_in = request.user.is_authenticated
    is_admin = request.user.is_authenticated and request.user.is_superuser
    return JsonResponse({'is_logged_in': is_logged_in, 'is_admin': is_admin})


@login_required(login_url='/login/oidc/')
def get_username(request):
    """ 
    Returns the username of the user. 
        Args:
            request (HttpRequest): The request object.
        Returns:
            JsonResponse: A JSON response containing the username.
    """
    username = request.user.social_auth.first().uid
    return JsonResponse({'username': username})
