"""Aqara Ceiling Light T1M (lumi.light.acn032) - RGB ring effects.

Upstream ZHA only exposes "power on state" for this light. This quirk keeps
that and adds the ring's dynamic effect settings, as reverse engineered by
Zigbee2MQTT (zigbee-herdsman-converters lumiT1MEffect, lumiRGBEffectSpeed,
lumiRGBEffectColors, lumiSegmentColors). All live on the Aqara manufacturer
cluster 0xFCC0, endpoint 1:

    0x051F effect          uint32  flow1, flow2, fading, hopping, breathing, rolling
    0x0520 effect_speed    uint8   0-100 %
    0x0522 segment_colors  octstr  4-byte segment mask, 4 zero bytes, 4-byte color
    0x0523 effect_colors   octstr  0x00, count, then 4 bytes per color (1-8)

Colors are CIE xy, each scaled to 0-65535 and sent big-endian (x then y).

"Effect" shows up as a select entity and "Effect speed" as a number entity.
The color attributes are byte strings, so they're written with the
zha.set_zigbee_cluster_attribute action. Pass them as a hex string prefixed
with "hex:" (the prefix stops Home Assistant from turning an all-digit hex
string into a number). The ring effect script blueprint in this repository
builds these strings for you.

Install: put this file in your ZHA custom quirks folder, e.g.

    zha:
      custom_quirks_path: /config/custom_zha_quirks/

and restart Home Assistant. The device page should then show
"Quirk: ...aqara_t1m_ring".
"""

from typing import Final

from zigpy import types as t
from zigpy.zcl.foundation import BaseAttributeDefs, DataTypeId, ZCLAttributeDef

from zhaquirks.builder import QuirkBuilder
from zhaquirks.xiaomi import AQARA, XiaomiAqaraE1Cluster


class HexBytes(t.LVBytes):
    """Octet string that can also be created from a hex string.

    Accepts bytes, or a string like "hex:0003a1b2..." (prefix optional,
    spaces ignored).
    """

    def __new__(cls, value=b""):
        if isinstance(value, str):
            text = value.strip()
            if text.lower().startswith("hex:"):
                text = text[4:]
            value = bytes.fromhex(text.replace(" ", ""))
        return super().__new__(cls, value)


class LumiPowerOnStateMode(t.enum8):
    """Power on state mode (same as upstream)."""

    On = 0x00
    LastState = 0x01
    Off = 0x02


class T1MRingEffect(t.enum32):
    """RGB ring dynamic effect."""

    flow1 = 0
    flow2 = 1
    fading = 2
    hopping = 3
    breathing = 4
    rolling = 5


class AqaraT1MRingCluster(XiaomiAqaraE1Cluster):
    """Aqara manufacturer cluster with T1M ring attributes."""

    class AttributeDefs(BaseAttributeDefs):
        """Manufacturer specific attributes."""

        power_on_state: Final = ZCLAttributeDef(
            id=0x0517,
            type=LumiPowerOnStateMode,
            zcl_type=DataTypeId.uint8,
            access="rw",
            is_manufacturer_specific=True,
        )
        effect: Final = ZCLAttributeDef(
            id=0x051F,
            type=T1MRingEffect,
            zcl_type=DataTypeId.uint32,
            access="rw",
            is_manufacturer_specific=True,
        )
        effect_speed: Final = ZCLAttributeDef(
            id=0x0520,
            type=t.uint8_t,
            access="rw",
            is_manufacturer_specific=True,
        )
        segment_colors: Final = ZCLAttributeDef(
            id=0x0522,
            type=HexBytes,
            zcl_type=DataTypeId.octstr,
            access="w",
            is_manufacturer_specific=True,
        )
        effect_colors: Final = ZCLAttributeDef(
            id=0x0523,
            type=HexBytes,
            zcl_type=DataTypeId.octstr,
            access="w",
            is_manufacturer_specific=True,
        )


(
    QuirkBuilder(AQARA, "lumi.light.acn032")
    .friendly_name(manufacturer="Aqara", model="Ceiling Light T1M")
    .replaces(AqaraT1MRingCluster)
    .replaces(AqaraT1MRingCluster, endpoint_id=2)
    .enum(
        AqaraT1MRingCluster.AttributeDefs.power_on_state.name,
        LumiPowerOnStateMode,
        AqaraT1MRingCluster.cluster_id,
        translation_key="power_on_state",
        fallback_name="Power on state",
    )
    .enum(
        AqaraT1MRingCluster.AttributeDefs.power_on_state.name,
        LumiPowerOnStateMode,
        AqaraT1MRingCluster.cluster_id,
        endpoint_id=2,
        translation_key="power_on_state",
        fallback_name="Power on state",
    )
    .enum(
        AqaraT1MRingCluster.AttributeDefs.effect.name,
        T1MRingEffect,
        AqaraT1MRingCluster.cluster_id,
        translation_key="ring_effect",
        fallback_name="Ring effect",
    )
    .number(
        AqaraT1MRingCluster.AttributeDefs.effect_speed.name,
        AqaraT1MRingCluster.cluster_id,
        min_value=0,
        max_value=100,
        step=1,
        unit="%",
        translation_key="ring_effect_speed",
        fallback_name="Ring effect speed",
    )
    .add_to_registry()
)
