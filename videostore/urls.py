from django.shortcuts import render
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.staff_entry, name='staff_entry'),  
    path('customer_staff_entry', views.customer_staff_entry, name='customer_staff_entry'),
    path('export-report/', views.export_report, name='export_report'),
    path('all_entries', views.all_entries, name='all_entries'),
    path('superadmin/', views.superadmin_dashboard, name='superadmin_dashboard'),
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('forbidden/', lambda request: render(request, 'forbidden.html'), name='forbidden'),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
