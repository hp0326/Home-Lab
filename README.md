# Home-Lab 
Segmented network with services: Linux router, DMZ with reverse proxy, hardening, infrastructure verifying script

## Network architecture
<img width="822" height="674" alt="Network architecture - three segmented zones" src="https://github.com/user-attachments/assets/1faf24cc-92ae-4f37-b942-30b8369eedff" />

## Technologies used
Ubuntu, nftables, dnsmasq, Docker, nginx, WireGuard, Python, PowerShell

## What this project demonstrates
* Designed a zone-segmented network with different levels of trust (LAN/DMZ/SERVERS) 
* Configured firewall rules according to the default-deny principle
* Automated server hardening (idempotent - safe to re-run)
* Built a custom multi-layer verification tool (ports/TLS/HTTP) for the lab infrastructure
  
## Problems & lessons learned
I tested verification script by intentionally breaking a service to see if the script would detect the failure. 
I stopped the container running the backend of a simple web app.

I noticed that the service still responded over HTTPS, because the script tested only if the TLS handshake is successful. 
The handshake itself is not enough, because it involves a proxy that terminates TLS locally and then queries the backend behind it.

To correctly test the verification script it should be done layer by layer (ports/TLS/HTTP) - each layer sees what lower layers can't, so I added an HTTP-status check.

## Components
**ad/** - PowerShell scripts for Active Directory administration:
* Audit.ps1 reports accounts without password requirement and privileged group members in the domain. 
* Create-Users.ps1 automates creating AD users from a CSV file, with validation and idempotency (skips accounts that already exist).
* System_details.ps1 provides information about the system such as OS version, RAM or free disk space.

**hardening/** - Idempotent Bash script created for hardening Linux servers (SSH key auth, firewall, fail2ban, auto-updates). It's safe to re-run.

**verify/** - Python script providing multi-layer verification (ports/TLS/HTTP) of the lab infrastructure with a report and a non-zero exit code on failure

**proxy/** - nginx reverse proxy configuration. Listens on port 443 with a self-signed TLS certificate. The proxy redirects HTTP to HTTPS (301).

**web1/** and **web2/** - simple HTML backends running in Docker containers behind the nginx reverse proxy.

## Technical details

Network addressing

| Area     | Subnet            | Gateway (router) | DHCP pool        |
|----------|-------------------|------------------|------------------|
| LAN      | 192.168.10.0/24   | 192.168.10.1     | .100 – .200      |
| DMZ      | 192.168.20.0/24   | 192.168.20.1     | static           |
| SERVERS  | 192.168.30.0/24   | 192.168.30.1     | static           |

Virtual Machines

Firewall rules



