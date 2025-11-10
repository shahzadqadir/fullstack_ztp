# ~/automation/fullstack_ztp/ztp/utility_functions.py

def create_host_file(host):
    file_path = f"/automation/ztp/host_vars/{host.hostname}.yml"
    try:
        with open(file_path, 'w') as file:
            file.write(f"hostname: {host.hostname}\n")
            file.write("users:\n")
            file.write(f"  - username: {host.device_username}\n")
            file.write(f"    password: {host.device_password}\n")
            file.write(f"    priv: 15\n")
            file.write(f"ip_domain: shahzadqadir.com\n")
            file.write(f"domain_lookup: false\n")
            file.write(f"auth: {host.auth_type}\n")
            file.write(f"enable_ssh: true\n")
            file.write("interfaces:\n")
            for interface in host.host_interfaces.all():
                file.write(f"  - name: {interface.name}\n")
                file.write(f"    descr: {interface.description}\n")
                file.write(f"    ip_address: {interface.ipaddress}\n")
                file.write(f"    mask: {interface.mask}\n")
                file.write(f"    state: {interface.state}\n")
            file.write("routing:\n")
            file.write("  bgp:\n")
            bgp = host.host_bgp.first()
            file.write(f"    local_as: {bgp.local_as}\n")
            file.write(f"    neighbors:\n")
            for neighbor in bgp.host_bgp_neighbors.all():
                file.write(f"      - ip: {neighbor.ipaddress}\n")
                file.write(f"        remote_as: {neighbor.remote_as}\n")
            file.write(f"    networks:\n")
            for network in bgp.host_bgp_networks.all():
                file.write(f"      - subnet: {network.subnet}\n")
                file.write(f"        mask: {network.mask}\n")
    except FileNotFoundError as e:
        return JsonResponse({
            "status": "error",
            "message": "Could not create file",
            "error": e
        })
    except PermissionError as e:
        return JsonResponse({
            "status": "error",
            "message": "Permission Denied",
            "error": e
        })
    except IsADirectoryError as e:
        return JsonResponse({
            "status": "error",
            "message": "Path points to a directory",
            "error": e
        }) 