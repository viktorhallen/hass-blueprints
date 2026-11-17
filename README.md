# hass-blueprints

Home Assistant blueprints.

## Blueprints

### IKEA BILRESA dual button (ZHA)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fviktorhallen%2Fhass-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fikea_bilresa_dual_button.yaml)

File: [blueprints/automation/ikea_bilresa_dual_button.yaml](blueprints/automation/ikea_bilresa_dual_button.yaml)

For the IKEA BILRESA two-button remote (model `09B9`) paired with ZHA.

| Button | Short press | Double press | Hold |
|---|---|---|---|
| **I** (top) | Light on | Custom action | Dim up until release |
| **O** (bottom) | Light off | Custom action | Dim down until release |

Every event (including hold and release) also has an optional custom action, so
the blueprint is usable without a light. Requires Home Assistant 2024.10 or newer.
