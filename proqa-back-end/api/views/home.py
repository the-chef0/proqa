from django.shortcuts import redirect
from django.conf import settings

def home(request):
    """
    Redirects to the login page.
        Args:
            request (HttpRequest): The request object.
        Returns:
            HttpResponseRedirect: A redirect to the login page.
    """
    return redirect(settings.LOGIN_REDIRECT_URL)
