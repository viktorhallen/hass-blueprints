"""IKEA BILRESA scroll wheel (E2490, model 09BA) - double and triple press.

Without a quirk, ZHA drops the remote's multi-press messages: they are a
manufacturer-specific command 0x07 on the client Scenes cluster, the same one
the BILRESA dual button (09B9) uses for double press. Replacing that cluster
with zhaquirks' IKEA ScenesCluster makes ZHA decode it and fire a zha_event:

    command: press, cluster_id: 5, endpoint_id: 1
    params.param1: 256 -> double press, 257 -> triple press

(mapping as in Zigbee2MQTT's ikeaBilresaDouble: 256 = on_double = double
press, 257 = off_double = triple press).

On/off presses and scrolling (move_to_level) are not touched.

Install: put this file in your ZHA custom quirks folder, e.g.

    zha:
      custom_quirks_path: /config/custom_zha_quirks/

and restart Home Assistant. The device page should then show
"Quirk: ...ikea_bilresa_scroll_wheel".
"""

from zigpy.zcl import ClusterType
from zigpy.zcl.clusters.general import Scenes

from zhaquirks.builder import QuirkBuilder
from zhaquirks.const import (
    BUTTON,
    CLUSTER_ID,
    COMMAND,
    COMMAND_PRESS,
    DOUBLE_PRESS,
    ENDPOINT_ID,
    PARAMS,
    TRIPLE_PRESS,
)
from zhaquirks.ikea import IKEA, ScenesCluster

(
    QuirkBuilder(IKEA, "09BA")
    .replaces(ScenesCluster, cluster_type=ClusterType.Client)
    .device_automation_triggers(
        {
            (DOUBLE_PRESS, BUTTON): {
                COMMAND: COMMAND_PRESS,
                CLUSTER_ID: Scenes.cluster_id,
                ENDPOINT_ID: 1,
                PARAMS: {"param1": 256},
            },
            (TRIPLE_PRESS, BUTTON): {
                COMMAND: COMMAND_PRESS,
                CLUSTER_ID: Scenes.cluster_id,
                ENDPOINT_ID: 1,
                PARAMS: {"param1": 257},
            },
        }
    )
    .add_to_registry()
)
