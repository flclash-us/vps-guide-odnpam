#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Subscription Converter - Transform proxy subscription links between formats"""

import base64
import json
import re
import sys
import yaml
from urllib.parse import urlparse, parse_qs
from dataclasses import dataclass

@dataclass
class ProxyNode:
    name: str
    server: str
    port: int
    protocol: str
    params: dict

    def to_clash(self):
        base = {"name": self.name, "server": self.server, "port": self.port}
        if self.protocol == "ss":
            base["type"] = "ss"
            base["cipher"] = self.params.get("cipher", "aes-256-gcm")
            base["password"] = self.params.get("password", "")
        elif self.protocol == "vmess":
            base["type"] = "vmess"
            base["uuid"] = self.params.get("uuid", "")
            base["alterId"] = int(self.params.get("alterId", 0))
            base["cipher"] = self.params.get("cipher", "auto")
        elif self.protocol == "trojan":
            base["type"] = "trojan"
            base["password"] = self.params.get("password", "")
        return base

class SubConverter:
    def __init__(self, subscription_url=None, content=None):
        self.url = subscription_url
        self.raw_content = content
        self.nodes = []

    def parse(self):
        if self.url and not self.raw_content:
            print(f"Fetching: {self.url}")
        content = self.raw_content or ""
        # Try base64 decode
        try:
            decoded = base64.b64decode(content).decode()
            if decoded.strip().startswith(("ss://", "vmess://", "trojan://")):
                content = decoded
        except Exception:
            pass
        # Parse lines
        for line in content.strip().split("\n"):
            line = line.strip()
            if line.startswith("ss://"):
                node = self._parse_ss(line)
            elif line.startswith("vmess://"):
                node = self._parse_vmess(line)
            elif line.startswith("trojan://"):
                node = self._parse_trojan(line)
            else:
                continue
            if node:
                self.nodes.append(node)
        return self.nodes

    def _parse_ss(self, uri):
        try:
            body = uri[5:]
            if "@" in body:
                userinfo, rest = body.split("@", 1)
                decoded = base64.b64decode(userinfo).decode()
                cipher, password = decoded.split(":", 1)
                host_port, name = rest.split("#", 1) if "#" in rest else (rest, "SS Node")
                host, port = host_port.rsplit(":", 1)
                return ProxyNode(name, host, int(port), "ss",
                               {"cipher": cipher, "password": password})
        except Exception:
            pass
        return None

    def _parse_vmess(self, uri):
        try:
            decoded = json.loads(base64.b64decode(uri[8:]))
            return ProxyNode(
                decoded.get("ps", "VMess Node"),
                decoded.get("add", ""),
                int(decoded.get("port", 443)),
                "vmess",
                {"uuid": decoded.get("id", ""), "alterId": decoded.get("aid", 0),
                 "cipher": decoded.get("scy", "auto"),
                 "network": decoded.get("net", "tcp"),
                 "tls": decoded.get("tls", "")}
            )
        except Exception:
            return None

    def _parse_trojan(self, uri):
        try:
            body = uri[9:]
            password, rest = body.split("@", 1)
            host_port = rest.split("?")[0].split("#")[0]
            host, port = host_port.rsplit(":", 1)
            return ProxyNode("Trojan Node", host, int(port), "trojan",
                           {"password": password})
        except Exception:
            return None

    def to_clash(self, **kwargs):
        proxies = [n.to_clash() for n in self.nodes]
        config = {
            "port": 7890, "socks-port": 7891, "mode": "rule",
            "proxies": proxies,
            "proxy-groups": [
                {"name": "Proxy", "type": "select",
                 "proxies": ["Auto"] + [p["name"] for p in proxies]},
                {"name": "Auto", "type": "url-test",
                 "proxies": [p["name"] for p in proxies],
                 "url": "http://www.gstatic.com/generate_204", "interval": 300}
            ],
            "rules": ["MATCH,Proxy"]
        }
        return yaml.dump(config, allow_unicode=True, default_flow_style=False)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Subscription Converter")
    parser.add_argument("--input", help="Subscription URL or file")
    parser.add_argument("--format", default="clash", help="Output format")
    parser.add_argument("--output", help="Output file")
    args = parser.parse_args()
    
    sc = SubConverter(subscription_url=args.input)
    if args.input and args.input.startswith("http"):
        print("URL mode - parse() would fetch the subscription")
    print(f"Output format: {args.format}")
