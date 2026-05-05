from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import NLCoordinator

_LOGGER = logging.getLogger(__name__)

SENSORS = [
    ("Brightness", "brightness", None, None, "mdi:brightness-6"),   # Helligkeit [0..255]
    ("Color Temp", "kelvin", SensorDeviceClass.TEMPERATURE, "K", "mdi:thermometer"),  # Kelvin (Farbtemperatur)
    ("Color (x,y)", "color", None, None, "mdi:palette"),          # Farbkoordinaten (keine Einheit)
]

async def async_setup_entry(hass, entry, async_add_entities):
    _LOGGER.debug("async_setup_entry")

    coordinator = hass.data[DOMAIN][entry.entry_id]
    inst_name = coordinator.entry.data["profile_name"]
    _LOGGER.debug(f"inst_name: {inst_name}")
    async_add_entities([
        NLSensor(coordinator, entry, inst_name, name, field, devcls, unit, icon)
        for name, field, devcls, unit, icon in SENSORS
    ])

class NLSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, coordinator, entry, inst_name, name, field, devcls, unit, icon):
        super().__init__(coordinator)
        self.inst_name = inst_name
        self._field = field

        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{self._field}"
        self._attr_device_class = devcls
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon

        _LOGGER.debug(f"Sensor {self._attr_unique_id} initiated")

    @property
    def native_value(self):
        data = self.coordinator.data
        if data is None:
            return None

        value = getattr(data, self._field)
        if self._field == "color" and value is not None:
            x, y = value
            return f"{x:.4f},{y:.4f}"

        return value

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.entry.entry_id)},
            "name": f"Natural Lights ({self.inst_name})",
            "manufacturer": "Uli",
            "model": "Natural Lights Engine",
        }
