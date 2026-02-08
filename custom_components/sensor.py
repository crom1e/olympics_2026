"""Sensor platform for 2026 Winter Olympics integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_COUNTRY, DOMAIN, PARTICIPATING_COUNTRIES


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    country_code = entry.data[CONF_COUNTRY]
    country_name = PARTICIPATING_COUNTRIES[country_code]

    sensors = [
        OlympicsMedalSensor(coordinator, country_code, country_name, "gold"),
        OlympicsMedalSensor(coordinator, country_code, country_name, "silver"),
        OlympicsMedalSensor(coordinator, country_code, country_name, "bronze"),
        OlympicsMedalSensor(coordinator, country_code, country_name, "total"),
        OlympicsRankSensor(coordinator, country_code, country_name),
    ]

    async_add_entities(sensors)


class OlympicsMedalSensor(CoordinatorEntity, SensorEntity):

    def __init__(
        self,
        coordinator,
        country_code: str,
        country_name: str,
        medal_type: str,
    ) -> None:
        super().__init__(coordinator)
        self._country_code = country_code
        self._country_name = country_name
        self._medal_type = medal_type
        self._attr_name = f"{country_name} {medal_type.capitalize()} Medals"
        self._attr_unique_id = f"{DOMAIN}_{country_code}_{medal_type}_medals"
        self._attr_icon = self._get_icon()
        self._attr_native_unit_of_measurement = "medals"
        self._attr_state_class = SensorStateClass.TOTAL

    def _get_icon(self) -> str:
        icons = {
            "gold": "mdi:medal",
            "silver": "mdi:medal-outline",
            "bronze": "mdi:medal",
            "total": "mdi:trophy",
        }
        return icons.get(self._medal_type, "mdi:medal")

    @property
    def native_value(self) -> int:
        if self.coordinator.data:
            return self.coordinator.data.get(self._medal_type, 0)
        return 0

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Return additional attributes."""
        if not self.coordinator.data:
            return {}

        attrs = {
            "country": self._country_name,
            "country_code": self._country_code,
            "rank": self.coordinator.data.get("rank", "-"),
        }

        if self._medal_type != "total":
            attrs.update(
                {
                    "gold": self.coordinator.data.get("gold", 0),
                    "silver": self.coordinator.data.get("silver", 0),
                    "bronze": self.coordinator.data.get("bronze", 0),
                    "total": self.coordinator.data.get("total", 0),
                }
            )

        return attrs

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._country_code)},
            "name": f"Olympics 2026 - {self._country_name}",
            "manufacturer": "2026 Winter Olympics",
            "model": "Medal Tracker",
            "entry_type": "service",
        }


class OlympicsRankSensor(CoordinatorEntity, SensorEntity):

    def __init__(
        self,
        coordinator,
        country_code: str,
        country_name: str,
    ) -> None:
        super().__init__(coordinator)
        self._country_code = country_code
        self._country_name = country_name
        self._attr_name = f"{country_name} Rank"
        self._attr_unique_id = f"{DOMAIN}_{country_code}_rank"
        self._attr_icon = "mdi:podium"

    @property
    def native_value(self) -> str:
        if self.coordinator.data:
            return self.coordinator.data.get("rank", "-")
        return "-"

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        if not self.coordinator.data:
            return {}

        return {
            "country": self._country_name,
            "country_code": self._country_code,
            "gold": self.coordinator.data.get("gold", 0),
            "silver": self.coordinator.data.get("silver", 0),
            "bronze": self.coordinator.data.get("bronze", 0),
            "total": self.coordinator.data.get("total", 0),
        }

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._country_code)},
            "name": f"Olympics 2026 - {self._country_name}",
            "manufacturer": "2026 Winter Olympics",
            "model": "Medal Tracker",
            "entry_type": "service",
        }
