import json

from .command_executor import show_quick_panel, run_command
from .notifier import log_info, log_error

def select_device(app_builder_command, on_device_selected):
    devices = []

    add_device_if_not_empty = lambda device: device != None and devices.append(device)
    on_device_data_reveived = lambda device_data: add_device_if_not_empty(_parse_device_data(device_data))
    on_devices_data_finished = lambda succeeded: _show_devices_list_and_select_device(app_builder_command, devices, on_device_selected) if succeeded else on_device_selected(None)

    run_command(["device", "--json"], on_device_data_reveived, on_devices_data_finished, True, "Retrieving devices")

def _parse_device_data(device_data):
    try:
        return json.loads(device_data)
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        log_error(device_data)
        return None

def _show_devices_list_and_select_device(app_builder_command, devices, on_device_selected):
    devicesCount = len(devices)
    if devicesCount == 0:
        log_info("There are no connected devices")
        on_device_selected(None)
    elif devicesCount == 1:
        on_device_selected(devices[0])
    elif devicesCount > 1:
        devicesList = list(map((lambda device: [device["displayName"] if device.get("displayName") else device["identifier"],
                "Platform: {platform} {version}".format(platform=device["platform"] if device.get("platform") else "", version=device["version"] if device.get("version") else ""),
                "Model: {model}".format(model=device["model"] if device.get("model") else ""),
                "Vendor: {vendor}".format(vendor=device["vendor"] if device.get("vendor") else "")]),
            devices))
        show_quick_panel(app_builder_command.get_window(), devicesList, lambda device_index: on_device_selected(devices[device_index]) if device_index >= 0 else on_device_selected(None))
