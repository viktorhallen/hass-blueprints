# Notes for agents

Home Assistant blueprints, imported into HA via the `source_url` / my.home-assistant
import links in README.md. Keep README's blueprint list in sync when adding or
renaming a blueprint, and keep `source_url` pointing at the file on `main`.

## Layout

- `blueprints/automation/*.yaml` — automation blueprints.
- `blueprints/script/*.yaml` — script blueprints (one script per preset).
- `zha_quirks/*.py` — custom ZHA quirks (v2 `QuirkBuilder`, imported from
  `zhaquirks.builder`) for devices where upstream ZHA is missing something.
  Candidates for upstreaming to zigpy/zha-device-handlers.

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

### IKEA BILRESA scroll wheel (E2490, `09BA`, no upstream quirk)

- No upstream ZHA quirk, so the blueprint matches raw `zha_event` `command`
  values rather than device triggers.
- Double / triple press: the remote sends manufacturer-specific Scenes command
  `0x07` (same as the dual button's double press), `param1` 256 = double,
  257 = triple (from Z2M's `ikeaBilresaDouble`: 256 → `on_double` = double
  press, 257 → `off_double` = triple press). Upstream ZHA drops it; our quirk
  `zha_quirks/ikea_bilresa_scroll_wheel.py` swaps in zhaquirks' IKEA
  `ScenesCluster` so it arrives as `zha_event` `command: press`. The quirk's
  device triggers only match on `param1` (the wheel's `param2` is unknown);
  the blueprint reads `param1` itself instead of relying on them.
  Long press sends nothing (per Z2M docs). Z2M also dedupes repeated multi-press
  messages; we don't yet. Quirk untested on a real device as of 2026-11-17.
- Press: the remote keeps an internal on/off state and alternates `on` / `off`
  commands. Treated as one toggle button (any light on → all off).
- Scroll: `move_to_level` with an **absolute** level (0–255, saturates at the
  ends). Level is read from `params.level`, falling back to `args`. The
  blueprint stores the last level in a user-provided `input_number` helper
  (blueprints can't create helpers) and applies the difference to each light.
  A repeated level ≥250 / ≤5 is read as "still scrolling past the end".
  `mode: queued` keeps the deltas in order.
- Unverified as of 2026-11-17: whether the remote keeps sending events at the
  ends (if it goes silent there, scrolling past the end can't work), the exact
  level range, and whether `move_to_level_with_on_off` is ever sent (handled
  just in case).
- User reported on 2026-11-17 that press and relative scroll dimming work on
  the real device.
- Bottom button = channel selector for 3 Zigbee groups (21658/21659/21660,
  LEDs show the active one). It sends nothing itself and only works after
  Touchlink-binding lights on 2+ channels. Neither Z2M nor (as far as we know)
  ZHA can tell which channel a command came from. Multi-press "scene" commands
  are documented by Z2M as going to group 65289. Untested here as of
  2026-11-19; the user plans to try unlocking a second channel.

### Aqara Ceiling Light T1M (`lumi.light.acn032`, ring effects)

- Upstream ZHA quirk (`zhaquirks.xiaomi.aqara.light_acn`) only adds
  `power_on_state` (0x0517). Our `zha_quirks/aqara_t1m_ring.py` replaces it,
  keeping that and adding (from Z2M `lumiT1MEffect` & co., all on cluster
  0xFCC0 endpoint 1, Lumi manufacturer code via `XiaomiAqaraE1Cluster`):
  0x051F `effect` (uint32: flow1, flow2, fading, hopping, breathing, rolling),
  0x0520 `effect_speed` (uint8 0–100), 0x0522 `segment_colors` and 0x0523
  `effect_colors` (octet strings). Z2M says the effect can't be read back.
- Writing octet strings from HA: `zha.set_zigbee_cluster_attribute` only
  accepts int/bool/str, and zha's `convert_zcl_value` does `type(value)` for
  `LVBytes` (no hex parsing). So the quirk uses a `HexBytes(LVBytes)` type
  that accepts a hex string. Values carry a `hex:` prefix because HA's native
  template types would turn an all-digit hex string into a number.
- Packet formats: effect_colors = `00`, count, then per color CIE x, y scaled
  to 0–65535 big-endian (sRGB → XYZ → xy, same math as Z2M). segment_colors =
  4-byte segment bitmask (segment 1 = MSB of byte 0, 26 segments), 4 zero
  bytes, 4-byte color, one write per color. Segment colors aren't in a
  blueprint yet.
- The script blueprint's color template was checked against a port of Z2M's
  encoder on 2026-11-19 (byte-for-byte match). Untested on the real light:
  whether the custom quirk overrides the upstream one, the write order
  (colors → effect → speed), and whether the uint32 effect write is accepted.
