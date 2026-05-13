#!/usr/bin/env bash
echo "========================================"
echo "  BBR 加速一键安装"
echo "========================================"
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p > /dev/null 2>&1
echo "BBR 已启用"
