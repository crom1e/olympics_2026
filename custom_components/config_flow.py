"""Config flow for 2026 Winter Olympics integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import CONF_COUNTRY, DOMAIN, PARTICIPATING_COUNTRIES


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            country_code = user_input[CONF_COUNTRY]
            await self.async_set_unique_id(f"{DOMAIN}_{country_code}")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"Olympics 2026 - {PARTICIPATING_COUNTRIES[country_code]}",
                data=user_input,
            )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_COUNTRY): vol.In(
                    {
                        code: name
                        for code, name in sorted(
                            PARTICIPATING_COUNTRIES.items(), key=lambda x: x[1]
                        )
                    }
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
