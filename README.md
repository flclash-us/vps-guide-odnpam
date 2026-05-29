[English] BBR/Speedbost/LatencyCatalyst acceleration configuration guide.

## Why Network Acceleration

Overseas VPS to mainland China has high latency and packet loss. Acceleration solutions significantly improve experience.

## BBR Acceleration

```bash
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p
```

Recommended Tools

- [Clash for Windows](https://clashforwindows.site/) - Most popular Clash GUI for Windows
- [ClashMI](https://clashmi.site/) - Lightweight multi-platform Clash client
- [FlClash](https://flclash.us/) - Modern proxy tool with multi-protocol support