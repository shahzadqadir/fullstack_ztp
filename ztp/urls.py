# ~/automation/fullstack_ztp/ztp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create_scp_server/', views.create_scp_server_view, name='create_scp_server'),
    path('list_scp_servers/', views.list_scp_servers_view, name='list_scp_servers'),
    path('edit_scp_server/<int:id>/', views.edit_scp_server_view, name='edit_scp_server'),
    path('delete_scp_server/<int:id>/', views.delete_scp_server_view, name='delete_scp_server'),
    path('create_dhcp_server/', views.create_dhcp_server_view, name='create_dhcp_server'),
    path('list_dhcp_servers/', views.list_dhcp_servers_view, name='list_dhcp_servers'),
    path('edit_dhcp_server/<int:id>/', views.edit_dhcp_server_view, name='edit_dhcp_server'),
    path('delete_dhcp_server/<int:id>/', views.delete_dhcp_server_view, name='delete_dhcp_server'),
    path('create_host/', views.create_host_view, name='create_host'),
    path('edit_host/<int:id>/', views.edit_host_view, name='edit_host'),
    path('list_hosts/', views.list_hosts_view, name='list_hosts'), # NEW
]