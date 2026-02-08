# 2026 Winter Olympics - Home Assistant Integration

Track your country's medal count from the 2026 Winter Olympics in Home Assistant.

## Features

- Country selection via UI dropdown
- Polls Wikipedia every 5 minutes (08:00-23:00 CET)
- 5 sensors per country: Gold, Silver, Bronze, Total, and Rank
- Works even if your country hasn't won medals yet
- All sensors grouped under one device

## Installation

[![Quick installation link](https://my.home-assistant.io/badges/hacs_repository.svg)][my-hacs]

Recommended installation is through [HACS][hacs]:

1. Either [use this link][my-hacs], or navigate to HACS integration and:
   - 'Explore & Download Repositories'
   - Search for '2026 Winter Olympics'
   - Download
2. Restart Home Assistant
3. Go to Settings > Devices and Services > Add Integration
4. Search for and select '2026 Winter Olympics' 
5. Proceed with the configuration

### Manual Installation

1. Copy the `custom_components/olympics_2026` folder to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

## Setup

1. Settings → Devices & Services
2. "+ Add Integration"
3. Search "2026 Winter Olympics"
4. Select your country

You can add multiple countries by repeating this.

## Sensors

Example for Norway:

| Entity ID | Name |
|-----------|------|
| `sensor.norway_gold_medals` | Gold medals |
| `sensor.norway_silver_medals` | Silver medals |
| `sensor.norway_bronze_medals` | Bronze medals |
| `sensor.norway_total_medals` | Total medals |
| `sensor.norway_rank` | Rank |

## Example Dashboard Cards

### Basic Entities Card

```yaml
type: entities
title: Norway - Winter Olympics 2026
entities:
  - sensor.norway_rank
  - sensor.norway_gold_medals
  - sensor.norway_silver_medals
  - sensor.norway_bronze_medals
  - sensor.norway_total_medals
```

### Stats Graph

```yaml
type: statistics-graph
title: Medal Progress
entities:
  - sensor.norway_gold_medals
  - sensor.norway_silver_medals
  - sensor.norway_bronze_medals
stat_types:
  - change
days_to_show: 30
```

## Automation Example

```yaml
automation:
  - alias: "Norway Won a Medal"
    trigger:
      - platform: state
        entity_id: sensor.norway_total_medals
    condition:
      - condition: template
        value_template: "{{ trigger.to_state.state | int > trigger.from_state.state | int }}"
    action:
      - service: notify.mobile_app
        data:
          title: "New Medal for Norway!"
          message: >
            Total: {{ states('sensor.norway_total_medals') }}
            (Gold: {{ states('sensor.norway_gold_medals') }} 
            Silver: {{ states('sensor.norway_silver_medals') }} 
            Bronze: {{ states('sensor.norway_bronze_medals') }})
```

## Configuration

Polls between 08:00-23:00 CET every 5 minutes. Outside these hours it returns cached data.

## Supported Countries

All 80+ participating countries are supported. See [const.py](const.py) for the complete list.

## Troubleshooting

**Sensors show 0:**
- Check if your country has won medals yet
- Verify it's within 08:00-23:00 CET
- Check HA logs for errors

**Integration not appearing:**
- Restart Home Assistant after installation
- Check file permissions
- Check logs for errors

## Technical Details

- Data source: Wikipedia medal table
- Update method: DataUpdateCoordinator
- Dependencies: BeautifulSoup4, lxml
- Polling: 08:00-23:00 CET only

---


[hacs]: https://hacs.xyz
[my-hacs]: https://my.home-assistant.io/redirect/hacs_repository/?owner=crom1e&repository=olympics_2026&category=integration