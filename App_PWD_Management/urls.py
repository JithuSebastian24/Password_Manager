from django.urls import path
from .views import RegisterView,LoginView,UserView,LogoutView,UserCreatePasswordView,UserGetPasswordView,UserUpdatePasswordView,UserDeletePasswordView


urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('createpwd', UserCreatePasswordView.as_view()),
    path('getpwd', UserGetPasswordView.as_view()),
    path('updatepwd/<str:pk>', UserUpdatePasswordView.as_view()),
    path('deletepwd/<str:pk>', UserDeletePasswordView.as_view()),
    
    
    
]
