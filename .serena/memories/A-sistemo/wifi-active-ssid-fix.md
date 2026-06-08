# Wi-Fi Active SSID Fix — A-sistemo

## Problem
`scan_networks()` used `nmcli connection show --active` which returns connection **profile names**, not SSIDs. The profile name may differ from the actual SSID, causing the connected network to not display in `wifi ls`.

## Fix
Extract the actual SSID from the connection profile's `802-11-wireless.ssid` setting:

```python
def _get_active_wifi_ssids() -> list[str]:
    result = run(
        ["nmcli", "-t", "-f", "NAME,TYPE", "connection", "show", "--active"],
        check=False,
    )
    ssids = []
    for line in result.stdout.splitlines():
        parts = line.split(":", 1)
        if len(parts) == 2 and parts[1] == "wifi":
            ssid = run(
                ["nmcli", "-g", "802-11-wireless.ssid", "connection", "show", parts[0]],
                check=False,
            ).stdout.strip()
            if ssid:
                ssids.append(ssid)
    return ssids
```

Then replace the inline fallback in `scan_networks()` with:
```python
    for ssid in _get_active_wifi_ssids():
        if ssid not in seen_ssids:
            networks.insert(0, WiFiNetwork(name=ssid, active=True))
```

## Why `802-11-wireless.ssid`
- This is the NetworkManager D-Bus setting name for the actual SSID
- Stored in the connection profile on disk — works even when network is out of range
- Reliable regardless of profile naming conventions

## Edge Cases Covered
- No active Wi-Fi → empty list, no insertion
- Profile name ≠ SSID → actual SSID from profile settings
- Out of scan range → reads from stored profile
- Multi-device → iterates all active wifi profiles
