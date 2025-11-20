# ~/automation/fullstack_ztp/ztp/models.py

from django.db import models


class Host(models.Model):
    hostname = models.CharField(max_length=255)
    mgmt_ip = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    device_username = models.CharField(max_length=255)
    device_password = models.CharField(max_length=255)
    auth_type = models.CharField(max_length=255)

    def __str__(self):
        return f"Host: {self.hostname}"

class SCPServer(models.Model):
    ip_address = models.CharField(max_length=255)
    base_dir = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"SCPServer: {self.ip_address}"


class DHCPServer(models.Model):
    ip_address = models.CharField(max_length=255)
    subnet = models.CharField(max_length=255)
    default_router = models.CharField(max_length=255)
    option67 = models.CharField(max_length=255)

    def __str__(self):
        return f"DHCPServer: {self.ip_address}"


class BGP(models.Model):
    local_as = models.CharField(max_length=255)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name='host_bgp')

    def __str__(self):
        return f"BGP: {self.local_as}"

class BGPNeighbor(models.Model):
    ip_address = models.CharField(max_length=255)
    remote_as = models.CharField(max_length=255)
    bgp = models.ForeignKey(BGP, on_delete=models.CASCADE, related_name='host_bgp_neighbors')

    def __str__(self):
        return f"BGPNeighbor: {self.ip_address}"
    

class BGPNetwork(models.Model):
    subnet = models.CharField(max_length=255)
    mask = models.CharField(max_length=255)
    bgp = models.ForeignKey(BGP, on_delete=models.CASCADE, related_name='host_bgp_networks')

    def __str__(self):
        return f"BGPNetwork: {self.subnet}"
    

class Interface(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=255)
    mask = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name='host_interfaces')

    def __str__(self):
        return f"Interface: {self.ip_address}"  


class StaticRoute(models.Model):
    destination = models.CharField(max_length=255)
    mask = models.CharField(max_length=255)
    next_hop = models.CharField(max_length=255)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name='host_static_routes')

    def __str__(self):
        return f"StaticRoute: {self.destination}"   