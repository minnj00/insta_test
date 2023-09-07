from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:pfuser_id>/follow-async/<int:user_id>/', views.follow_async, name='follow_async'),
    path('<username>/', views.profile, name='profile'),
    path('<username>/follow/', views.follow, name='follow'),
    # path('<username>/followers/', views.followers, name='followers'),
    # path('<username>/following/', views.followings, name='followings'),
   

]