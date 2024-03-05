from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('account-recovery/', views.account_recovery, name='account_recovery'),
    path('logout/', views.logout_view, name='logout'),
    path('recovery/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         views.recovery, name='recovery'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         views.activate, name='activate'),
]
