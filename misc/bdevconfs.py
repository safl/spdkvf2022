#!/usr/bin/env python3
from pathlib import Path
import pprint
import json

SYSTEMS = {
    "gen3": [
        {"pcie": "0000:41:00.0", "os": "0n1", "label": "M10_16GB"},
        {"pcie": "0000:42:00.0", "os": "1n1", "label": "M10_16GB"},
        {"pcie": "0000:43:00.0", "os": "2n1", "label": "M10_16GB"},
        {"pcie": "0000:44:00.0", "os": "3n1", "label": "M10_16GB"},
        {"pcie": "0000:45:00.0", "os": "4n1", "label": "980PRO_2TB"},
        {"pcie": "0000:46:00.0", "os": "5n1", "label": "980PRO_2TB"},
        {"pcie": "0000:47:00.0", "os": "6n1", "label": "980PRO_2TB"},
        {"pcie": "0000:48:00.0", "os": "7n1", "label": "980PRO_2TB"},
    ],
    "gen4": [
        {"pcie": "0000:05:00.0", "os": "3n1", "label": "M10_16GB"},
        {"pcie": "0000:07:00.0", "os": "4n1", "label": "M10_16GB"},
        {"pcie": "0000:01:00.0", "os": "0n1", "label": "M10_16GB"},
        {"pcie": "0000:09:00.0", "os": "5n1", "label": "980PRO_512GB"},
        {"pcie": "0000:0a:00.0", "os": "6n1", "label": "980PRO_1TB"},
        {"pcie": "0000:02:00.0", "os": "1n1", "label": "980PRO_1TB"},
        {"pcie": "0000:03:00.0", "os": "2n1", "label": "980PRO_1TB"},
    ],
}

IOPATHS = {
    "driver": {
        "bdev_name": "bdev_nvme",
        "io_mechanism": "nvme",
        "method": "bdev_nvme_attach_controller",
    },
    "aio": {
        "bdev_name": "bdev_aio",
        "io_mechanism": "libaio",
        "method": "bdev_aio_create",
    },
    "uring": {
        "bdev_name": "bdev_uring",
        "io_mechanism": "io_uring",
        "method": "bdev_uring_create",
    },
    "xnvme_libaio": {
        "bdev_name": "bdev_xnvme",
        "io_mechanism": "libaio",
        "method": "bdev_xnvme_create",
    },
    "xnmve_io_uring": {
        "bdev_name": "bdev_xnvme",
        "io_mechanism": "io_uring",
        "method": "bdev_xnvme_create",
    },
    "xnvme_io_uring_cmd": {
        "bdev_name": "bdev_xnvme",
        "io_mechanism": "io_uring",
        "method": "bdev_xnvme_create",
    },
}


def main():

    for iopath_label, iopath in IOPATHS.items():
        for sys_label, devices in SYSTEMS.items():

            conf = {"subsystems": []}
            for count, dev_info in enumerate(devices, 1):
                bdevs = {
                    "subsystem": "bdev",
                    "config": [],
                }

                params = {}

                # Setup the "handle"
                if "driver" in iopath_label:
                    params["trtype"] = "PCIe"
                    params["traddr"] = f"{dev_info['pcie']}"
                elif "io_uring_cmd" in iopath_label:
                    params["filename"] = f"/dev/ng{dev_info['os']}"
                else:
                    params["filename"] = f"/dev/nvme{dev_info['os']}"

                # Set "extras" for xNVMe
                if "xnvme" in iopath_label:
                    params["io_mechanism"] = f"{dev_info['io_mechanism']}"
                    # params["conserve_cpu"] = False

                bdev_name_instance = "_".join(
                    [
                        "bdev",
                        f"{bdev_name}",
                        f"{io_mechanism}",
                        f"device{dev_info['os']}",
                    ]
                )

                if io_mechanism == "io_uring":
                    filename = f"/dev/nvme{dev_info['os']}"
                elif io_mechanism == "io_uring_cmd":
                    filename = f"/dev/ng{dev_info['os']}"

                bdev = {
                    "params": {
                        "filename": filename,
                        "name": bdev_name_instance,
                        "io_mechanism": f"{io_mechanism}",
                        "conserve_cpu": False,
                    },
                    "method": iopath["method"],
                }

                bdevs["config"].append(bdev)

                conf["subsystems"].append(bdevs)

                filename = Path(
                    f"{sys_label}_bdev_{bdev_name}_{io_mechanism}_{count}.json"
                )

                print(filename)
                pprint.pprint(conf)


if __name__ == "__main__":
    main()
