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

