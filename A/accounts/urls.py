from django.urls import path
from accounts import views



app_name = 'accounts'
urlpatterns = [
    path('register/',views.UserRegisterView.as_view(),name='user_register'),
    path('login/',views.UserLoginView.as_view(),name='user_login'),
    path('logout/',views.UserLogoutView.as_view(),name='user_logout'),
    path('profile/<int:user_id>/',views.UserProfileView.as_view(),name='user_profile'),
    path('edit/',views.UserEditeProfileView.as_view(),name='edit_profile'),
]
