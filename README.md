# Sub Converter Tool a65asg

A powerful subscription conversion tool that transforms proxy subscription links between different client formats.

## Supported Formats

| Source | Target |
|--------|--------|
| Any | Clash YAML |
| Any | V2Ray JSON |
| Any | Surge CONF |
| Any | Quantumult X |
| Any | Surfboard |
| Any | Sing-Box |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Convert subscription
python convert.py --input "YOUR_SUB_URL" --format clash --output config.yaml

# Convert to multiple formats
python convert.py --input "YOUR_SUB_URL" --format clash,v2ray,surge --output-dir ./configs/

# With custom rules
python convert.py --input "YOUR_SUB_URL" --format clash --rules custom_rules.yaml
```

## API Usage

```python
from converter import SubConverter

# Initialize converter
sc = SubConverter(subscription_url="YOUR_SUB_URL")

# Convert to Clash format
clash_config = sc.to_clash(
    rule_provider=True,
    proxy_group_strategy="url-test",
    dns_mode="fake-ip"
)

# Convert to V2Ray format
v2ray_config = sc.to_v2ray(
    outbound_protocol="vmess",
    transport="ws"
)

# Save to file
sc.save(clash_config, "config.yaml")
```

## Features

- Auto-detect subscription format (base64, clash yaml, sip002)
- Merge multiple subscriptions
- Custom rule sets and proxy groups
- Filter nodes by keyword or regex
- Sort nodes by speed/region/protocol
- Built-in rule providers (China, AdBlock, Streaming)

## Configuration

```yaml
# converter_config.yaml
general:
  log_level: info
  cache_enabled: true
  
subscription:
  merge_strategy: append  # append | replace | dedup
  filter_keywords: ["过期", "官网", "流量"]
  
proxy_groups:
  - name: "Auto"
    type: url-test
    filter: "香港|HK"
    tolerance: 50
    
  - name: "Streaming"
    type: select
    filter: "美国|US"
    
rules:
  - "DOMAIN-SUFFIX,google.com,Proxy"
  - "DOMAIN-KEYWORD,netflix,Streaming"
  - "GEOIP,CN,DIRECT"
  - "MATCH,Proxy"
```

## Recommended Tools

- [Clash for Windows](https://clashforwindows.site/) - Best proxy client for Windows/Mac/Linux
- [Clash for Windows](https://clashforwindows.site/) - Most popular Clash GUI
- [ClashMI](https://clashmi.site/) - Lightweight Clash client
- [FlClash](https://flclash.us/) - Modern proxy tool

## License

MIT License
