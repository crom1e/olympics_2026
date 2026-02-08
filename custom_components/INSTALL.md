# Installation Guide

## Quick Start

1. **Copy files to your Home Assistant**
   ```bash
   # Installation path:
   # config/custom_components/olympics_2026/
   ```

2. **Restart Home Assistant**
   - Settings → System → Restart

3. **Add the integration**
   - Settings → Devices & Services
   - "+ Add Integration"
   - Search "2026 Winter Olympics"
   - Select your country

4. **View sensors**
   - Example: `sensor.norway_gold_medals`
   - All grouped under one device

## Verify Installation

Check files:

```bash
ls -la config/custom_components/olympics_2026/
```

Should have:
- `__init__.py`
- `config_flow.py`
- `const.py`
- `manifest.json`
- `sensor.py`
- `strings.json`
- `translations/en.json`

## Multiple Countries

Add more countries by repeating the integration setup.

4. Select a different country
5. Repeat as needed

Each country gets its own device with 5 sensors.

## Dashboard Setup

Copy from `lovelace-example.yaml` or use:

```yaml
type: entities
title: Norway - Olympics 2026
entities:
  - sensor.norway_rank
  - sensor.norway_gold_medals
  - sensor.norway_silver_medals
  - sensor.norway_bronze_medals
  - sensor.norway_total_medals
```

## Troubleshooting

**Integration doesn't appear:**
- Restart Home Assistant
- Clear browser cache

**Sensors show "Unknown":**
- Outside 08:00-23:00 CET
- Network issues
- Check logs: `ha core logs`

**Country has no medals yet:**
- This is normal, sensors will show 0 and rank "-"

## Uninstall

1. Settings → Devices & Services → Delete entries
2. Remove folder: `config/custom_components/olympics_2026`
3. Restart

## Advanced

Change update interval or hours in `const.py`:
```python
UPDATE_INTERVAL = 300  # seconds
START_HOUR = 8
END_HOUR = 23
```
