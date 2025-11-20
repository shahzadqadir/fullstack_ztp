# ~/automation/fullstack_ztp/ztp/admin.py

from django.contrib import admin

from .models import BGP, BGPNeighbor, BGPNetwork, Interface, StaticRoute, Host

admin.site.register(BGP)
admin.site.register(BGPNeighbor)
admin.site.register(BGPNetwork)
admin.site.register(Interface)
admin.site.register(StaticRoute)
admin.site.register(Host)