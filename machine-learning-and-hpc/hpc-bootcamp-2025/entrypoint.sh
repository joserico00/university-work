#!/bin/bash

set -e

echo "[*] Starting VPN Agent..."

WG_CONF="/etc/wireguard/wg0.conf"
WG_KEY_DIR="/etc/wireguard/keys"
mkdir -p $WG_KEY_DIR

# Generate keypair if not exist
if [ ! -f "$WG_KEY_DIR/privatekey" ]; then
    echo "[*] Generating WireGuard keypair..."
    umask 077
    wg genkey | tee "$WG_KEY_DIR/privatekey" | wg pubkey > "$WG_KEY_DIR/publickey"
fi

PRIVATE_KEY=$(cat "$WG_KEY_DIR/privatekey")

cat > $WG_CONF <<EOF
[Interface]
PrivateKey = ${PRIVATE_KEY}
Address = ${WG_ADDRESS}
PostUp = iptables -t nat -A POSTROUTING -o ${WG_IFACE} -j MASQUERADE
PostDown = iptables -t nat -D POSTROUTING -o ${WG_IFACE} -j MASQUERADE

[Peer]
PublicKey = ${WG_SERVER_PUBLIC_KEY}
Endpoint = ${WG_SERVER_ENDPOINT}
AllowedIPs = ${WG_ALLOWED_IPS}
PersistentKeepalive = ${WG_KEEPALIVE}
EOF

echo "[✓] Public Key for registration:"
cat "$WG_KEY_DIR/publickey"

echo 1 > /proc/sys/net/ipv4/ip_forward

wg-quick up wg0

tail -f /dev/null
