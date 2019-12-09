from django.urls import path
from .views import *
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    path('<int:pk>/', PostDetail.as_view()),
    path('', PostList.as_view()),
    path('users/current_user/', get_current_user),
    path('users/', CreateUserView.as_view()  ),
    path('users/list', GetAllUserAndProfiles.as_view()),
    path('auth-jwt-refresh/', refresh_jwt_token),
]