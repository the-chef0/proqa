from django.urls import path
from api import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout/", views.logout_view, name="logout"),
    path("check-login/", views.check_login_status, name="check_login_status"),
    path("get-csrf-token/", views.csrf_token_view, name="get_csrf_token"),
    path("get-username/", views.get_username, name="get_username"),
    path("text-stream/", views.text_stream, name="text_stream")
]
