# Home-Lab 
Segmented network with services: Linux router, DMZ with reverse proxy, hardening, infrastructure verifying script

## Technologies used
Ubuntu, nftables, dnsmasq, Docker, nginx, WireGuard, Python, PowerShell

## Network architecture
<img width="759" height="661" alt="Network architecture - three segmented zones" src="https://github.com/user-attachments/assets/b6cdd9c2-dcf7-4177-bdb9-a8415bd4cafe" />

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

