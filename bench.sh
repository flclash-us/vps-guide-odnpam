#!/usr/bin/env bash
echo "========================================"
echo "  VPS 基准测试"
echo "========================================"
echo "[系统信息]"
echo "OS: $(uname -o) $(uname -r)"
echo "CPU: $(nproc) vCPU"
echo ""
echo "[磁盘 I/O]"
dd if=/dev/zero of=/tmp/dd_test bs=1M count=512 oflag=direct 2>&1 | tail -1
rm -f /tmp/dd_test
