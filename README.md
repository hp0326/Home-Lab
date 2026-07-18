# Home-Lab 
Segmented network with services: Linux router, DMZ with reverse proxy, hardening, infrastructure verifying script

## Project objective

## Technologies used
Ubuntu, nftables, dnsmasq, Docker, nginx, WireGuard, Python, PowerShell

## Network architecture
<img width="759" height="660" alt="diagram drawio" src="https://github.com/user-attachments/assets/22a9a1a0-661f-40e1-9a01-d5b8ab9bb0fc" />

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

