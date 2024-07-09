from django.urls import include, path

from login_system.views import custom_login, custom_register_view, doctor_dashboard, patient_dashboard, index_view
app_name = 'home'

urlpatterns = [
    path('', index_view, name='home'),
    path('register/', custom_register_view, name='register'),
    path('login/', custom_login, name='login'),
    path('patienddashboard/', patient_dashboard, name='patienddashboard'),
    path('doctordashboard/', doctor_dashboard, name='doctordashboard'),
    
   
    
]