# Home-Lab 
Segmented network with services: Linux router, DMZ with reverse proxy, hardening, infrastructure verifying script

## Network architecture
<img width="759" height="661" alt="Network architecture - three segmented zones" src="https://github.com/user-attachments/assets/7f8c8f2d-5053-47ea-9e59-1566ca5cb7ee" />

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

## Status

## Technical details

Network addressing

| Area     | Subnet            | Gateway (router) | DHCP pool        |
|----------|-------------------|------------------|------------------|
| LAN      | 192.168.10.0/24   | 192.168.10.1     | .100 – .200      |
| DMZ      | 192.168.20.0/24   | 192.168.20.1     | static           |
| SERVERS  | 192.168.30.0/24   | 192.168.30.1     | static           |

Virtual Machines

Firewall rules

DNS and DHCP

