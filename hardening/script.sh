#!/usr/bin/env bash
set -euo pipefail

ADMIN_USER="admin"
SSH_PUBKEY="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHKX0J4C0vJHGRPEQZIUegw8D1vSVOtdT/JreLtLIR91 router@client"

log() { echo "[*] $*"; }

if [[ $EUID -ne 0  ]]; then
        echo "Script must be run as root" >&2
        exit 1
fi

create_user() {

        log "Creating user"

        if ! id "$ADMIN_USER" >&/dev/null; then
                useradd "$ADMIN_USER" -m -s /bin/bash
        else
                log "User "$ADMIN_USER" already exists"
        fi

        usermod -aG sudo "$ADMIN_USER"

        mkdir -p /home/"$ADMIN_USER"/.ssh
        echo "$SSH_PUBKEY" > /home/"$ADMIN_USER"/.ssh/authorized_keys

        chown -R "$ADMIN_USER":"$ADMIN_USER" /home/"$ADMIN_USER"/.ssh
        chmod 700 /home/"$ADMIN_USER"/.ssh
        chmod 600 /home/"$ADMIN_USER"/.ssh/authorized_keys

}

setup_firewall() {

        log "Setting up firewall"

        cat > /etc/nftables.conf <<'EOF'
#!/usr/sbin/nft -f

flush ruleset

table inet filter {
        chain input {
                type filter hook input priority filter; policy drop;

                iif lo accept
                ct state established,related accept
                tcp dport 22 accept

        }

        chain forward {
                type filter hook forward priority filter; policy drop;

        }

        chain output {
                type filter hook output priority filter; policy accept;

        }
}
EOF

        nft -f /etc/nftables.conf

        systemctl enable nftables

}

harden_ssh() {

	log "Hardening ssh"

	cat > /etc/ssh/sshd_config.d/99-hardening.conf <<'EOF'
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
EOF

	sshd -t
	systemctl reload-on-restart ssh

}

setup_fail2ban() {

	log "Setting up fail2ban"

	export DEBIAN_FRONTEND=noninteractive

	apt-get update
	apt-get install fail2ban -y

	cat > /etc/fail2ban/jail.local <<'EOF'
[sshd]
enabled=true
port=ssh
maxretry=4
findtime=600
bantime=3600
ignoreip=127.0.0.1/8 192.168.10.0/24
EOF

	systemctl restart fail2ban
	systemctl enable fail2ban

}

#main

create_user
setup_firewall
harden_ssh
setup_fail2ban
