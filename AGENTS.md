# Notes for agents

Home Assistant blueprints, imported into HA via the `source_url` / my.home-assistant
import links in README.md. Keep README's blueprint list in sync when adding or
renaming a blueprint, and keep `source_url` pointing at the file on `main`.

## Layout

- `blueprints/automation/*.yaml` — automation blueprints.

## Conventions

- Target HA 2024.10+ syntax (`triggers:` / `trigger:` / `actions:` / `action:`).
- For ZHA remotes, use **device triggers** (`trigger: device`, `domain: zha`,
  `type` / `subtype`) rather than raw `zha_event` command matching. The
  type/subtype pairs come from the device's zhaquirks quirk
  (`device_automation_triggers`) and are what the HA logbook shows, e.g.
  "Remote Button Short Press - Turn On" = `remote_button_short_press` / `turn_on`.
- Empty optional action inputs are run with `choose: []` + `default: !input x`.

## Device notes

### IKEA BILRESA dual button (`09B9`, quirk `zhaquirks.ikea.bilresa2btn`)

- Triggers: short press `turn_on`/`turn_off`; double press, long press and long
  release `dim_up`/`dim_down`. All on endpoint 1.
- While held, the remote re-sends the long-press (Move) message about once a
  second, so the long-press trigger fires repeatedly. The blueprint uses
  `mode: restart` so repeats and the release cancel the dim loop; a max-steps
  input guards against a lost release.
- Dimming down with `brightness_step_pct` all the way turns the light off.
  Accepted for now (no clamp to a minimum brightness).
- Not yet tested on a real device as of 2026-11-17.
