# Home-Lab 
Segmented network with services: Linux router, DMZ with reverse proxy, hardening, infrastructure verifying script

## Technologies used
Ubuntu, nftables, dnsmasq, Docker, nginx, WireGuard, Python, PowerShell

## Network architecture
<img width="458" height="382" alt="Diagram bez tytułu drawio" src="https://github.com/user-attachments/assets/72091c07-e910-49a7-b186-78bba1a979dd" />

## Network addressing

| Area     | Subnet            | Gateway (router) | DHCP pool        |
|----------|-------------------|------------------|------------------|
| LAN      | 192.168.10.0/24   | 192.168.10.1     | .100 – .200      |
| DMZ      | 192.168.20.0/24   | 192.168.20.1     | static           |
| SERVERS  | 192.168.30.0/24   | 192.168.30.1     | static           |

## Virtual Machines

## Services in DMZ

## Firewall rules

## DNS and DHCP

