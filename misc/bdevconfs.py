#!/usr/bin/env python3
import argparse
from pathlib import Path
import pprint
import json
import os

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
        "io_mechanism": "spdk_nvme",
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
    "xnvme_io_uring": {
        "bdev_name": "bdev_xnvme",
        "io_mechanism": "io_uring",
        "method": "bdev_xnvme_create",
    },
    "xnvme_io_uring_cmd": {
        "bdev_name": "bdev_xnvme",
        "io_mechanism": "io_uring_cmd",
        "method": "bdev_xnvme_create",
    },
}


def gen_bdev_confs(args):

    for iopath_label, iopath in IOPATHS.items():
        for sys_label, devices in SYSTEMS.items():

            conf = {"subsystems": []}
            for count, dev_info in enumerate(devices, 1):
                bdevs = {
                    "subsystem": "bdev",
                    "config": [],
                }

                # Parameters, first the device "handle"
                params = {}
                if "driver" in iopath_label:
                    params["trtype"] = "PCIe"
                    params["traddr"] = f"{dev_info['pcie']}"
                elif "io_uring_cmd" in iopath_label:
                    params["filename"] = f"/dev/ng{dev_info['os']}"
                else:
                    params["filename"] = f"/dev/nvme{dev_info['os']}"

                # Parameters, then an instance name
                params["name"] = "_".join(
                    [
                        f"{iopath['bdev_name']}",
                        f"{iopath['io_mechanism']}",
                        f"device{dev_info['os']}",
                    ]
                )

                # Parameters, for xNVMe
                if "xnvme" in iopath_label:
                    params["io_mechanism"] = f"{iopath['io_mechanism']}"
                    # params["conserve_cpu"] = False

                bdevs["config"].append(
                    {
                        "params": params,
                        "method": iopath["method"],
                    }
                )
                conf["subsystems"].append(bdevs)

                output_dir = args.output / f"{sys_label}"
                os.makedirs(output_dir, exist_ok=True)

                filename = output_dir / "_".join(
                    [
                        f"{iopath['bdev_name']}",
                        f"{iopath['io_mechanism']}",
                        f"{count}.conf",
                    ]
                )

                with filename.open("w") as config:
                    json.dump(conf, config, indent=2, sort_keys=False)


def gen_commands(args):

    command = "taskset -c 0,1 t/io_uring -b512 -d128 -c16 -s16 -p1 -F1 -B1 -n2 -r10"
    pass


def parse_args():

    parser = argparse.ArgumentParser(
        prog="stuff", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--bdev-confs",
        action="store_true",
        help="Monitor workflow-output at '-o / --output'.",
    )
    parser.add_argument(
        "--commands",
        action="store_true",
        help="Monitor workflow-output at '-o / --output'.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default="/tmp",
        help="Path to the Configuration file.",
    )

    return parser.parse_args()


def main():

    args = parse_args()

    if args.bdev_confs:
        gen_bdev_confs(args)

    if args.commands:
        gen_commands(args)


if __name__ == "__main__":
    main()
