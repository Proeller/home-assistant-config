from __future__ import annotations

import logging

from datetime import time, timedelta
from dataclasses import dataclass
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.event import (
    async_track_state_change_event,
    async_track_time_interval,
)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .cie import (CIELuv, XYB, XY)
from .const import *

_LOGGER = logging.getLogger(__name__)

SUN_ENTITY = "sun.sun"

@dataclass
class Sensors:
    brightness: int    # 0..255
    kelvin: int
    color: tuple[float, float] | None

    def __init__(self, bri: int, kelv: int, x: float, y: float):
        self.brightness = bri
        self.kelvin = kelv
        self.color = (x, y)

@dataclass
class Point:
    time: float
    brightness: int   # 0..255
    kelvin: int
    color: XY

class NLCoordinator(DataUpdateCoordinator[Sensors]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        _LOGGER.debug("Initiating NLCoordinator")
        self.hass = hass
        self.entry = entry

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=None,  # wir triggern selber
        )

        self.points = [ Point(0.0, 200, 4000, XY(0.405, 0.390))]
        self._unsubs = []
        _LOGGER.debug("NLCoordinator initiated")

    async def async_config_entry_first_refresh(self) -> None:
        _LOGGER.debug("config_entry_first_refresh")

        # 1) Listener auf Inputs
        self._unsubs.append(
            async_track_state_change_event(
                self.hass,
                [SUN_ENTITY, ],
                self._handle_input_change,
            )
        )

        # 2) Zeittrigger z.B. alle 60s, damit Uhrzeit/Sonne weich interpolieren kann
        self._unsubs.append(
            async_track_time_interval(
                self.hass, self._handle_time_tick, timedelta(seconds=60)
            )
        )

        profile = self.entry.data["profile"]
        for dp in profile["points"]:
            self.add_datapoint(dp)
        self.points.sort(key = lambda x: x.time)

        _LOGGER.debug(f"{len(self.points)} data points loaded")
        _LOGGER.debug(f"Points: {str(self.points)}")

        # initial berechnen
        await self._async_recompute_and_update()

    async def async_shutdown(self) -> None:
        for u in self._unsubs:
            u()
        self._unsubs.clear()

    @callback
    def _handle_input_change(self, event) -> None:
        _LOGGER.debug("_handle_input_change")
        self.hass.async_create_task(self._async_recompute_and_update())

    @callback
    def _handle_time_tick(self, now) -> None:
        _LOGGER.debug("_handle_time_tick")
        self.hass.async_create_task(self._async_recompute_and_update())

    async def _async_recompute_and_update(self) -> None:
        self.data = self._compute_sensors()
        self.async_set_updated_data(self.data)

    def add_datapoint(self, dp) -> None:
        tme = time.fromisoformat(dp["time"])
        ftme = tme.hour + (tme.minute / 60.0)
        col = dp["color"]
        xy = XY(col["x"], col["y"])
        self.points.append(Point(ftme, dp["bright"], dp["kelvin"], xy))

    def _compute_sensors(self) -> Sensors | None:
        if len(self.points) < 2:
            return None

        now = dt_util.now()
        time = now.hour + now.minute / 60.0

        p1: Point = next((x for x in reversed(self.points) if x.time <= time))
        p2: Point = next((x for x in self.points if x.time > time), self.points[0])

        fixed_time = time if time >= p1.time else time + 24
        frac = (fixed_time - p1.time) / (p2.time - p1.time)
        _LOGGER.debug(f"now={fixed_time}; time1={p1.time}; time2={p2.time}; frac={frac:.2f}")

        xyb1 = XYB(p1.color, p1.brightness)
        _LOGGER.debug(f"xyb1={xyb1}")

        xyb2 = XYB(p2.color, p2.brightness)
        _LOGGER.debug(f"xyb2={xyb2}")

        color: XYB = self.xy_interpolate(xyb1, xyb2, frac)
        kelvin: int = round(self.interpolate(p1.kelvin, p2.kelvin, frac))

        _LOGGER.debug(f"Brightness={color.b}; kelvin={kelvin}; color={color}")
        return Sensors(color.b, kelvin, color.x, color.y)

    def interpolate(self, first: float, second: float, frac: float) -> float:
        return first + (second - first) * frac

    def xy_interpolate(self, first: XYB, second: XYB, frac: float) -> XYB:
        Luv1 = first.To_CIELuv()
        Luv2 = second.To_CIELuv()

        L = self.interpolate(Luv1.L, Luv2.L, frac)
        u = self.interpolate(Luv1.u, Luv2.u, frac)
        v = self.interpolate(Luv1.v, Luv2.v, frac)

        LuvR = CIELuv(L, u, v)
        xyB_Result = LuvR.To_xyB()
        return xyB_Result

