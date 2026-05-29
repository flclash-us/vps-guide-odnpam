#!/bin/bash
# TCP network optimization script - one-click BBR and kernel parameter tuning

cat >> /etc/sysctl.conf << '''EOF'''
# BBR Acceleration
net.core.default_qdisc=fq
net.ipv4.tcp_congestion_control=bbr

# Connection optimization
net.core.rm_max=2500000
net.core.netdev_max_backlog=2500000
net.ipv4.tcp_max_syn_backlog=8192
net.ipv4.tcp_fin_timeout=15
net.ipv4.tcp_fastopen=3
net.ipv4.tcp_mtu_probing=1
EOF

sysctl -p
echo "TCP optimization complete"