from __future__ import annotations

import json
import logging
import asyncio

from typing import Any
from pathlib import Path
from homeassistant import config_entries
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
import voluptuous as vol


from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class NLConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1
    MINOR_VERSION = 1

#---------------------------------------------------------------------------------------

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        _LOGGER.debug("async_step_user")

        errors: dict[str, str] = {}

        profiles = self.get_profiles()

        if not profiles:
            errors["base"] = "no_profiles_found"

        if user_input is not None:
            profile_name = user_input["profile"]
            _LOGGER.debug(f"set_unique_id: {profile_name}")
            await self.async_set_unique_id(profile_name)
            self._abort_if_unique_id_configured()
            return await self.async_create_entry_from_profile(profile_name)

        schema = vol.Schema({
            vol.Required("profile"): SelectSelector(
                SelectSelectorConfig(
                    options=list(profiles.keys()),
                    mode="dropdown"
                )
            )
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

#---------------------------------------------------------------------------------------

    async def async_step_import(self, user_input: dict[str, Any] | None = None):
        if user_input is None:
            return self.async_abort(reason="no_data")

        profile_name = user_input["profile"]
        await self.async_set_unique_id(profile_name)
        data = self.hass.data.setdefault(DOMAIN, {})
        data.setdefault("__yaml__", set()).add(self.unique_id)

        for entry in self._async_current_entries():
            if entry.unique_id == self.unique_id:
                self.hass.config_entries.async_update_entry(entry, data=user_input)
                self._abort_if_unique_id_configured()

        return self.async_create_entry(title=profile_name, data=user_input)

#---------------------------------------------------------------------------------------

    async def async_create_entry_from_profile(self, profile_name):
        loop = asyncio.get_running_loop()
        profile_data = await loop.run_in_executor(None, self.load_profile, profile_name)
        _LOGGER.debug(f"Profile data loaded: {str(profile_data)}")

        return self.async_create_entry(
            title=f"Natural Lights – {profile_name}",
            data={
                "profile_name": profile_name,
                "profile": profile_data,   # 👈 DAS ist entscheidend
            },
        )

#---------------------------------------------------------------------------------------

    def get_profiles(self):
        data_dir = Path(
            self.hass.config.path(
                "custom_components",
                "natural_lights",
                "data"
            )
        )

        if not data_dir.exists():
            return {}

        return {
            file.stem: file.name
            for file in sorted(data_dir.glob("*.json"))
            if file.is_file()
        }

#---------------------------------------------------------------------------------------

    def load_profile(self, profile_name):
        path = Path(
            self.hass.config.path(
                "custom_components",
                "natural_lights",
                "data",
                f"{profile_name}.json"
            )
        )

        if not path.exists():
            raise ValueError("Profile file not found")

        with path.open(encoding="utf-8") as f:
            data = json.load(f)

            # Minimal-Validierung (Beispiel)
        if "points" not in data:
            raise ValueError("Invalid profile format")

        return data
