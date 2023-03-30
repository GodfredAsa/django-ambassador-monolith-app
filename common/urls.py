from django.urls import path
from .views import (LoginApiView, RegisterApiView,
                    UserApiView, LogoutApiView, ProfileInfoApiView,
                    PasswordUpdateApiView
                    )
urlpatterns = [

    path('register', RegisterApiView.as_view()),
    path('login', LoginApiView.as_view()),
    path('user', UserApiView.as_view()),
    path('logout', LogoutApiView.as_view()),
    path('users/profile', ProfileInfoApiView.as_view()),
    path('users/password', PasswordUpdateApiView.as_view()),

]
