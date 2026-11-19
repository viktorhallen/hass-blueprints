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

### IKEA BILRESA scroll wheel (ZHA)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fviktorhallen%2Fhass-blueprints%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fikea_bilresa_scroll_wheel.yaml)

File: [blueprints/automation/ikea_bilresa_scroll_wheel.yaml](blueprints/automation/ikea_bilresa_scroll_wheel.yaml)

For the IKEA BILRESA scroll wheel (E2490, model `09BA`) paired with ZHA.

- **Press:** toggles the lights (any on → all off, otherwise all on).
- **Scroll:** dims relative to each light's current brightness, and keeps
  dimming when the remote's own level is stuck at its top or bottom.
- **Double / triple press:** custom actions, with the ZHA quirk below.

Needs a Number helper (0–255, step 1) per remote to remember the remote's last
level. Optional custom actions for press and scroll. Requires Home Assistant
2024.10 or newer.

#### ZHA quirk for double and triple press

Out of the box ZHA drops the scroll wheel's double and triple presses (Zigbee2MQTT
supports them). [zha_quirks/ikea_bilresa_scroll_wheel.py](zha_quirks/ikea_bilresa_scroll_wheel.py)
adds them:

1. Copy the file to e.g. `/config/custom_zha_quirks/`.
2. Point ZHA at that folder in `configuration.yaml`:

   ```yaml
   zha:
     custom_quirks_path: /config/custom_zha_quirks/
   ```

3. Restart Home Assistant. The device page should show
   `Quirk: ...ikea_bilresa_scroll_wheel`. If it doesn't, remove and re-pair the
   remote.

### Aqara T1M ring effect (ZHA, script)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fviktorhallen%2Fhass-blueprints%2Fblob%2Fmain%2Fblueprints%2Fscript%2Faqara_t1m_ring_effect.yaml)

File: [blueprints/script/aqara_t1m_ring_effect.yaml](blueprints/script/aqara_t1m_ring_effect.yaml)

Starts a dynamic effect on the RGB ring of the Aqara Ceiling Light T1M
(`lumi.light.acn032`). Each script made from it is one preset: effect (flow 1,
flow 2, fading, hopping, breathing, rolling), speed, ring brightness and 1–4
colors. Run it from a dashboard or an automation. Stop the effect by setting the
ring to a plain color or turning it off.

Requires the ZHA quirk [zha_quirks/aqara_t1m_ring.py](zha_quirks/aqara_t1m_ring.py),
installed the same way as the scroll wheel quirk above (device page should show
`Quirk: ...aqara_t1m_ring`). The quirk also adds **Ring effect** and **Ring
effect speed** controls to the light's device page.
