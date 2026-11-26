# HomeYantric

HomeYantric devices run ESP-IDF firmware and share a provisioning portal, LAN discovery, and a browser UI. This directory is the firmware build root (formerly `bed-controller-idf/`). Open it in your IDE and run ESP-IDF commands here.

| Device | Implementation |
| --- | --- |
| Adjustable bed | [Bed control](components/bed_control/) handles motion, limits, and presets. See the [pin assignments](docs/pin-assignments.md) and [wiring notes](docs/bed-wiring.md). |
| Lights | [Light control](components/light_control/) drives the LED hardware. The UI groups discovered lights by room. |
| Watering | Discovery-only pump profile. The Watering tab lists each controller and its configured outlet count. |

The [build guide](docs/how-to-build.md) lists role and board profiles. Start with a fresh build directory after moving an existing checkout because CMake caches absolute paths. The existing firmware project and binary name is `elev8_controller`.

[Wi-Fi provisioning](components/wifiProvisioning/) joins the device to the network. The [network manager](components/network_manager/) serves the API and advertises device roles over mDNS. The [web UI](data/) displays local and discovered devices. The [bed RF lab](labs/bed-rf/) contains independently buildable experiments.

## Watering design

A watering controller owns one pump. The single-plant variant has one outlet and a flow meter. The multi-plant variant selects one of three or four outlets using a servo-operated pinch valve. With a shared flow meter, select one outlet at a time so each measured dose belongs to one plant.

The intended first hardware milestone is a measured manual dose with a no-flow cutoff and maximum runtime. Local schedules, persistent dose history, and calibrated servo selection are subsequent milestones.
