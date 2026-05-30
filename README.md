# WireGuard VPN 搭建完全指南

WireGuard 是新一代 VPN 协议，以轻量、高速、简单著称。

## 为什么选择 WireGuard

- 高速: 比 OpenVPN 快数倍
- 安全: 现代加密算法（Curve25519）
- 轻量: 代码仅约 4000 行
- 跨平台: 支持所有主流系统

## 安装

```bash
# Ubuntu / Debian
apt update && apt install wireguard -y

# CentOS
yum install epel-release -y
yum install wireguard-tools -y
```

## 服务端配置

### 1. 生成密钥

```bash
cd /etc/wireguard
wg genkey | tee server_private.key | wg pubkey > server_public.key
chmod 600 server_private.key
```

### 2. 创建配置文件

```ini
# /etc/wireguard/wg0.conf
[Interface]
PrivateKey = <server_private_key>
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

[Peer]
PublicKey = <client_public_key>
AllowedIPs = 10.0.0.2/32
```

### 3. 启动

```bash
systemctl enable wg-quick@wg0
systemctl start wg-quick@wg0
```

## 对比 OpenVPN

| 特性 | WireGuard | OpenVPN |
|------|-----------|---------|
| 速度 | 极快 | 较慢 |
| 代码量 | ~4000行 | ~100万行 |
| 配置 | 简单 | 复杂 |

## 常见问题

**无法连接？** 检查防火墙是否放行 51820/UDP 端口。

---

推荐工具：

- [Clash for Windows](https://clashforwindows.site/)
- [ClashMI](https://clashmi.site/)
- [FlClash](https://flclash.us/)
