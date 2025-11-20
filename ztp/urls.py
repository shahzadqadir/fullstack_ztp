# ~/automation/fullstack_ztp/ztp/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('create_scp_server/', views.create_scp_server_view, name='create_scp_server'),
    path('list_scp_servers/', views.list_scp_servers_view, name='list_scp_servers'),
    path('edit_scp_server/<int:id>/', views.edit_scp_server_view, name='edit_scp_server'),
    path('delete_scp_server/<int:id>/', views.delete_scp_server_view, name='delete_scp_server'),    # NEW
]