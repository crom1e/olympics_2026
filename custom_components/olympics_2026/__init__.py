"""The 2026 Winter Olympics integration."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import async_timeout
import requests
from bs4 import BeautifulSoup

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_COUNTRY,
    COUNTRY_NAME_MAPPING,
    DOMAIN,
    END_HOUR,
    PARTICIPATING_COUNTRIES,
    START_HOUR,
    UPDATE_INTERVAL,
    WIKIPEDIA_URL,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]
SERVICE_FORCE_REFRESH = "force_refresh"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = OlympicsDataUpdateCoordinator(hass, entry)
    coordinator.force_refresh = True
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    async def handle_force_refresh(call: ServiceCall) -> None:
        country = call.data.get("country")
        for entry_id, coord in hass.data[DOMAIN].items():
            if coord.country_code == country or country == "all":
                coord.force_refresh = True
                await coord.async_request_refresh()

    hass.services.async_register(
        DOMAIN, SERVICE_FORCE_REFRESH, handle_force_refresh
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class OlympicsDataUpdateCoordinator(DataUpdateCoordinator):

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.country_code = entry.data[CONF_COUNTRY]
        self.country_name = PARTICIPATING_COUNTRIES[self.country_code]
        self.force_refresh = False

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{self.country_code}",
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    def _is_within_operating_hours(self) -> bool:
        cet_tz = ZoneInfo("Europe/Paris")
        now = datetime.now(cet_tz)
        return START_HOUR <= now.hour <= END_HOUR

    async def _async_update_data(self):
        if not self._is_within_operating_hours() and not self.force_refresh:
            _LOGGER.debug(
                "Outside operating hours (%s:00-%s:00 CET), using cached data",
                START_HOUR,
                END_HOUR,
            )
            if self.data:
                return self.data
            return self._get_zero_medals()

        try:
            async with async_timeout.timeout(30):
                medal_data = await self.hass.async_add_executor_job(
                    self._fetch_medal_table
                )
                self.force_refresh = False
                return medal_data

        except Exception as err:
            self.force_refresh = False
            raise UpdateFailed(f"Error fetching medal data: {err}") from err

    def _fetch_medal_table(self) -> dict:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; HomeAssistant-OlympicsIntegration/1.0)"
            }
            response = requests.get(WIKIPEDIA_URL, headers=headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            medal_table = soup.find("table", {"class": ["wikitable", "sortable"]})

            if not medal_table:
                _LOGGER.error("Could not find medal table on Wikipedia page")
                return self._get_zero_medals()

            rows = medal_table.find_all("tr")[1:]
            last_rank = "-"

            for row in rows:
                cols = row.find_all(["td", "th"])
                if len(cols) < 4:
                    continue

                try:
                    first_col = cols[0]
                    
                    if first_col.name == "td" and first_col.get_text(strip=True).isdigit():
                        rank_text = first_col.get_text(strip=True)
                        last_rank = rank_text
                        country_cell = cols[1]
                        medal_offset = 2
                    else:
                        country_cell = cols[0]
                        medal_offset = 1

                    country_link = country_cell.find("a")
                    country_name = (
                        country_link.get_text(strip=True)
                        if country_link
                        else country_cell.get_text(strip=True)
                    )

                    _LOGGER.debug("Found country: %s (rank: %s)", country_name, last_rank)

                    if self._matches_country(country_name):
                        if len(cols) >= medal_offset + 3:
                            gold = int(cols[medal_offset].get_text(strip=True) or 0)
                            silver = int(cols[medal_offset + 1].get_text(strip=True) or 0)
                            bronze = int(cols[medal_offset + 2].get_text(strip=True) or 0)

                            return {
                                "rank": last_rank,
                                "gold": gold,
                                "silver": silver,
                                "bronze": bronze,
                                "total": gold + silver + bronze,
                            }

                except (ValueError, IndexError, AttributeError) as e:
                    _LOGGER.warning("Error parsing row: %s", e)
                    continue

            _LOGGER.info(
                "%s not yet in medal table, returning zeros", self.country_name
            )
            return self._get_zero_medals()

        except requests.RequestException as err:
            _LOGGER.error("Error fetching Wikipedia page: %s", err)
            raise UpdateFailed(f"Error fetching data: {err}") from err

    def _matches_country(self, wiki_name: str) -> bool:
        if wiki_name == self.country_name:
            return True

        if wiki_name in COUNTRY_NAME_MAPPING:
            return COUNTRY_NAME_MAPPING[wiki_name] == self.country_code

        return False

    def _get_zero_medals(self) -> dict:
        return {
            "rank": "-",
            "gold": 0,
            "silver": 0,
            "bronze": 0,
            "total": 0,
        }
