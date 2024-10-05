from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'myapp1'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name = 'login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    
    path('my-investments/', my_investments, name='my_investments'),
    
    path('microshare-calculation/<int:startup_id>/', microshare_calculation, name='microshare_calculation'),

    path('solar-panel-cost/<int:startup_id>/', solar_panel_cost_calculation, name='solar_panel_cost'),
    
    
    
    path('startups/', StartupListView.as_view(), name='startup_list'),
    path('investment/',inverstment, name = 'investment'),




    path('startupdetail/<int:pk>',startupdetail,name = 'startupdetail'),





    #invest_create
    path('invest_create/',invest_create, name = 'invest_create'),





    path('startups/<int:pk>/', StartupDetailView.as_view(), name='startup_detail'),
    path('startups/<int:pk>/invest/', invest_in_startup, name='invest_in_startup'),
    path('login/',auth_views.LoginView.as_view(), name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(), name = 'logout'),
   
]

