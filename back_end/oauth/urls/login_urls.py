from django.urls import path
from oauth.views.login_view import *

urlpatterns = [
    # access_point uris => access to auth info..
    path('login', Login.as_view()), #ok
]