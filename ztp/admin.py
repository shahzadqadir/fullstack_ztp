# ~/automation/fullstack_ztp/ztp/admin.py

from django.contrib import admin

from .models import BGP, BGPNeighbor, BGPNetwork, Interface, StaticRoute, Host


class BGPAdmin(admin.ModelAdmin):
    list_display = ('local_as', 'host')

class BGPNeighborAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'remote_as', 'bgp')

class BGPNetworkAdmin(admin.ModelAdmin):
    list_display = ('subnet', 'mask', 'bgp')


class InterfaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'ip_address', 'state', 'host')


class StaticRouteAdmin(admin.ModelAdmin):    
    list_display = ('destination', 'mask', 'next_hop', 'host')


class HostAdmin(admin.ModelAdmin):
        list_display = ('hostname', 'mgmt_ip')

admin.site.register(BGP, BGPAdmin)
admin.site.register(BGPNeighbor, BGPNeighborAdmin)
admin.site.register(BGPNetwork, BGPNetworkAdmin)
admin.site.register(Interface, InterfaceAdmin)
admin.site.register(StaticRoute, StaticRouteAdmin)
admin.site.register(Host, HostAdmin)

