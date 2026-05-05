from __future__ import annotations
from .cie import XY

DOMAIN = "natural_lights"
DEFAULT_NAME = "Natural Lights"
PLATFORMS = ["sensor"]  # später z.B. ["sensor", "switch"]

XY_COLOR1 = XY(0.328, 0.334)
XY_COLOR2 = XY(0.401, 0.359)
XY_COLOR3 = XY(0.328, 0.334)
XY_COLOR4 = XY(0.575, 0.389)
XY_COLOR5 = XY(0.561, 0.4042)
XY_COLOR6 = XY(0.561, 0.4042)

KELVIN1 = 6410
KELVIN2 = 4291
KELVIN3 = 2890
KELVIN4 = 2237
KELVIN5 = 2217
KELVIN6 = 2217

BRIGHTNESS1 = 255
BRIGHTNESS2 = 255
BRIGHTNESS3 = 200
BRIGHTNESS4 = 143
BRIGHTNESS5 = 90
BRIGHTNESS6 = 25

TIME1 = "06:00:00"
TIME2 = "10:00:00"
TIME3 = "16:00:00"
TIME4 = "20:00:00"
TIME5 = "22:00:00"
TIME6 = "00:00:00"

HUE_COLORS = {
    # --- Red Area ---
    "red":              {"x": 0.675, "y": 0.322, "bri": 255},
    "scarlet":          {"x": 0.673, "y": 0.273, "bri": 255},
    "deep_red":         {"x": 0.640, "y": 0.330, "bri": 230},
    "pink":             {"x": 0.382, "y": 0.160, "bri": 255},
    "magenta":          {"x": 0.385, "y": 0.180, "bri": 255},
    "rose":             {"x": 0.345, "y": 0.210, "bri": 255},

    # --- Purple/Violet ---
    "purple":           {"x": 0.273, "y": 0.109, "bri": 255},
    "lavender":         {"x": 0.300, "y": 0.150, "bri": 255},
    "ultraviolet":      {"x": 0.240, "y": 0.085, "bri": 220},
    "violet":           {"x": 0.245, "y": 0.130, "bri": 240},

    # --- Blue Area ---
    "blue":             {"x": 0.167, "y": 0.040, "bri": 255},
    "royal_blue":       {"x": 0.161, "y": 0.031, "bri": 255},
    "sky_blue":         {"x": 0.255, "y": 0.155, "bri": 255},
    "ice_blue":         {"x": 0.275, "y": 0.240, "bri": 255},

    # --- Green Area ---
    "green":            {"x": 0.172, "y": 0.746, "bri": 255},
    "lime":             {"x": 0.409, "y": 0.518, "bri": 255},
    "leaf_green":       {"x": 0.275, "y": 0.665, "bri": 255},
    "mint":             {"x": 0.300, "y": 0.560, "bri": 255},

    # --- Yellow Area ---
    "yellow":           {"x": 0.444, "y": 0.516, "bri": 255},
    "amber":            {"x": 0.501, "y": 0.399, "bri": 255},
    "warm_yellow":      {"x": 0.472, "y": 0.450, "bri": 255},

    # --- Orange Area ---
    "orange":           {"x": 0.572, "y": 0.404, "bri": 255},
    "deep_orange":      {"x": 0.600, "y": 0.382, "bri": 255},
    "sunset":           {"x": 0.561, "y": 0.404, "bri": 220},

    # --- White Tones (converted from CCT) ---
    "candle":           {"x": 0.533, "y": 0.414, "bri": 200},  # ~2000K
    "warm_white":       {"x": 0.458, "y": 0.410, "bri": 255},  # ~2700K
    "soft_white":       {"x": 0.436, "y": 0.404, "bri": 255},  # ~3000K
    "neutral_white":    {"x": 0.405, "y": 0.390, "bri": 255},  # ~3500K
    "cool_white":       {"x": 0.380, "y": 0.380, "bri": 255},  # ~4000K
    "daylight":         {"x": 0.344, "y": 0.358, "bri": 255},  # ~5000K
    "cool_daylight":    {"x": 0.315, "y": 0.325, "bri": 255},  # ~6500K
}
