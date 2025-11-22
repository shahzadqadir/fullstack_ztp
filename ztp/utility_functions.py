# ~/automation/fullstack_ztp/ztp/utility_functions.py

import subprocess
import os
from django.http import JsonResponse

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
                file.write(f"    ip_address: {interface.ip_address}\n")
                file.write(f"    mask: {interface.mask}\n")
                file.write(f"    state: {interface.state}\n")
            file.write("routing:\n")
            file.write("  bgp:\n")
            bgp = host.host_bgp.first()
            file.write(f"    local_as: {bgp.local_as}\n")
            file.write(f"    neighbors:\n")
            for neighbor in bgp.host_bgp_neighbors.all():
                file.write(f"      - ip: {neighbor.ip_address}\n")
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
    

def update_inventory(host):
    if os.path.exists('/automation/ztp/hosts'):
        with open('/automation/ztp/hosts', 'a') as file:
            file.write(f"\n{host.hostname}  ansible_connection=local")


def create_playbook(hostname, tftp_server, playbook_path):
    
    try:
        with open(playbook_path, 'w') as file:
            file.write(f"# PLAY 1\n")
            file.write(f"- name: Create Configurations for Cisco Devices\n")
            file.write(f"  hosts: {hostname}\n")
            file.write(f"  gather_facts: no\n")
            file.write(f"  tasks:\n")

            file.write(f"    - name: Generate Device Configs\n")
            file.write(f"      template:\n")
            file.write(f"        src: templates/ztp_host.j2\n")
            file.write(f"        dest: config_files/{hostname}.cfg\n")

            file.write(f"# PLAY 2\n")
            file.write(f"- name: Transfer device configs to TFTP Server\n")
            file.write(f"  hosts: r1\n")
            file.write(f"  gather_facts: no\n")

            file.write(f"  tasks:\n")
            file.write(f"    - name: Copy configs to TFTP Server\n")
            file.write(f"      command: scp config_files/{hostname}.cfg script@{tftp_server}:/disk0:/{hostname}.cfg\n")

            file.write(f"# PLAY 3\n")
            file.write(f"- name: Configure TFTP/DHCP Servers\n")
            file.write(f"  hosts: r1\n")
            file.write(f"  gather_facts: no\n")

            file.write(f"  tasks:\n")

            file.write(f"    - name: Update DHCP to new config file\n")
            file.write(f"      cisco.ios.ios_config:\n")
            file.write(f"        lines:\n")
            file.write(f"          - network 10.10.99.0 /24\n")
            file.write(f"          - default-router 10.10.99.254\n")
            file.write(f"          - option 150 ip 10.10.99.254\n")
            file.write(f"          - option 67 ascii {hostname}.cfg\n")
            file.write(f"        parents: ip dhcp pool MGMT-POOL\n")
    
            file.write(f"    - name: Update TFTP to config file\n")
            file.write(f"      cisco.ios.ios_config:\n")
            file.write(f"        lines:\n")
            file.write(f"          - tftp-server {hostname}.cfg\n")
            file.write(f"          - ip dhcp excluded-address 10.10.99.1 10.10.99.100\n")
            file.write(f"          - ip dhcp excluded-address 10.10.99.201 10.10.99.254\n")
        return JsonResponse({
            "status": "success",
            "message": "Playbook created successfully"
        })
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
    

def run_playbook(playbook_path, inventory_path):
    playbook_dir = os.path.dirname(playbook_path)
    try:
        result = subprocess.run(
            ["/usr/local/bin/ansible-playbook", "-i", inventory_path, playbook_path],
            capture_output=True, text=True, check=True, cwd=playbook_dir
        )
        return JsonResponse({
            "status": "success",
            "message": "Playbook executed successfully",
            "stdout": result.stdout
        }, status=200)
    except subprocess.CalledProcessError as e:
        print(e.stderr)    
        return JsonResponse({
            "status": "error",
            "message": "Playbook execution failed",
            "stderr": e.stderr
        }, status=500)