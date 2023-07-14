from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """Session authentication with csrf disabled."""

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
