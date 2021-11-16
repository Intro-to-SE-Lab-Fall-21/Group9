from django.urls import path
from . import views
from .views import inbox
app_name = "emails"   


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("homepage/", views.homepage, name="homepage"),
    path("homepage", views.homepage, name="homepage"),
    path("register/", views.register_request, name="register"),
    path("register", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("login", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),
    path("logout", views.logout_request, name= "logout"),
    path("inbox/", views.inbox ,name="inbox"),
    path("inbox", views.inbox ,name="inbox"),
    path("compose/",views.compose,name="compose"),
    path("compose",views.compose,name="compose")]