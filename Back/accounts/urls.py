from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


urlpatterns = [
    path('login/', views.loginAPI, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.logoutAPI, name='logout'),
    path('users/', views.UserViewSet.as_view({'get': 'list'}), name='users'),
]