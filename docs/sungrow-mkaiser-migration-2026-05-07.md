# Sungrow MKaiser migration baseline 2026-05-07

Branch: `migrate-mkaiser-current`

MKaiser source: `mkaiser/Sungrow-SHx-Inverter-Modbus-Home-Assistant`

Source revision: `63beec6770e8275670cdf01437cb305817f32988`

Captured before migration deployment, after correcting the previous WR2 offset and WR1 battery capacity:

| Entity | State |
| --- | ---: |
| `sensor.wr1_total_pv_generation` | `40067.3 kWh` |
| `sensor.wr2_total_power_yield` | `2211.9 kWh` |
| `sensor.wr2_total_pv_generation_corrected` | `24040.1 kWh` |
| `sensor.total_pv_generation` | `64107.4 kWh` |
| `sensor.wr1_battery_capacity` | `22.4 kWh` |
| `sensor.wr1_battery_charge` | `9.7 kWh` |
| `sensor.wr1_battery_current` | `-5.1 A` |
| `sensor.wr2_nominal_active_power` | `6.0 kW` |
| `sensor.wr1_battery_level` | `49.2 %` |
| `sensor.wr1_min_soc` | `12.0 %` |
| `sensor.wr1_max_soc` | `100.0 %` |

Expected normalized yield:

| Inverter | Generator | Yield | kWh/kWp |
| --- | ---: | ---: | ---: |
| WR1 | `12.45 kWp` | `40067.3 kWh` | `3218.3` |
| WR2 corrected | `7.47 kWp` | `24040.1 kWh` | `3218.2` |

The expected WR1/WR2 ratio is `1.667` (`12.45 / 7.47`).

## After deployment

Captured after deploying the MKaiser 2026 files and reloading templates:

| Entity | State |
| --- | ---: |
| `sensor.total_pv_generation_inv_1` | `40067.7 kWh` |
| `sensor.total_pv_generation_battery_discharge_inv_2` | `2211.9 kWh` |
| `sensor.wr2_total_pv_generation_corrected` | `24040.1 kWh` |
| `sensor.total_pv_generation` | `64107.8 kWh` |
| `sensor.battery_capacity_high_precision_inv_1` | `22.40 kWh` |
| `sensor.battery_charge_inv_1` | `10.15 kWh` |
| `sensor.battery_current_inv_1` | `-8.9 A` |
| `sensor.inverter_rated_output_inv_2` | `6000 W` |
| `sensor.total_dc_power_inv_1` | `3206 W` |
| `sensor.total_dc_power_inv_2` | `1876 W` |
| `sensor.total_dc_power` | `5082 W` |

After normalized yield:

| Inverter | Generator | Yield | kWh/kWp |
| --- | ---: | ---: | ---: |
| WR1 | `12.45 kWp` | `40067.7 kWh` | `3218.3` |
| WR2 corrected | `7.47 kWp` | `24040.1 kWh` | `3218.2` |

After migration WR1/WR2 ratio: `1.667`.
