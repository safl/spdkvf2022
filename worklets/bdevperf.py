#!/usr/bin/env python
"""
    Run fio...
"""
import json
import logging as log
import os
import shutil
import traceback
from itertools import product
from pathlib import Path

"""
from cijoe.fio.wrapper import fio_fancy

def spdk_opts_to_spdk_conf(spdk_opts, parent):

    spdk_conf = {
        "subsystems": [
            {
                "subsystem": "bdev",
                "config": [
                    {
                        "params": spdk_opts["params"],
                        "method": f"bdev_{spdk_opts['bdev']}_create",
                    }
                ],
            }
        ]
    }

    conf_filestem = "_".join(
        [
            "spdk",
            "bdev",
            spdk_opts["bdev"],
            spdk_opts["params"].get("io_mechanism", "foo"),
        ]
    )

    spdk_conf_path = Path(parent) / f"{conf_filestem}.conf"
    with spdk_conf_path.open("w") as scpath:
        json.dump(spdk_conf, scpath)

    return conf_filestem, spdk_conf_path, spdk_conf

"""


def worklet_entry(args, cijoe, step):

    repetitions = step.get("with", {}).get("repetitions", 3)
    iosizes = step.get("with", {}).get("iosizes", ["4K"])
    iodepths = step.get("with", {}).get("iodepths", [1, 2, 4, 8])
    bdev_conf_root = step.get("with", {}).get("bdev_confs", "/tmp")

    iopaths = {
        "io_uring_cmd-bdev_xnvme": {
            "bdev_name": "bdev_xnvme",
            "io_mechanism": "io_uring_cmd",
        },
        "io_uring-bdev_uring": {
            "bdev_name": "bdev_uring",
            "io_mechanism": "io_uring",
        },
        "io_uring-bdev_xnvme": {
            "bdev_name": "bdev_xnvme",
            "io_mechanism": "io_uring",
        },
        "libaio-bdev_aio": {
            "bdev_name": "bdev_aio",
            "io_mechanism": "libaio",
        },
        "libaio-bdev_xnvme": {
            "bdev_name": "bdev_xnvme",
            "io_mechanism": "libaio",
        },
    }

    artifacts = Path(args.output) / "artifacts"
    os.makedirs(str(artifacts), exist_ok=True)

    err = 0
    try:
        for (bs, iodepth, (label, params), rep) in product(
            iosizes, iodepths, iopaths.items(), range(repetitions)
        ):
            bdevperf_output_path = (
                artifacts
                / f"bdevperf-output_BS={bs}_IODEPTH={iodepth}_LABEL={label}_{rep}.txt"
            )

            # Create a spdk-configuration file and transfer it
            spdk_conf_path = Path(bdev_conf_root) / "_".join(
                [
                    params["bdev_name"],
                    params["io_mechanism"],
                    "1.conf",
                ]
            )

            # Run bdevperf
            command = [
                "/root/git/spdk/test/bdev/bdevperf/bdevperf",
                f"--json {spdk_conf_path}",
                f"-q {iodepth}",
                f"-o {bs}",
                "-w randread",
                "-t 10",
                "-m '[0]'",
            ]
            err, state = cijoe.run(" ".join(command))
            if err:
                log.error(f"failed: {state}")

            # Save the bdevperf output to a file in artifacts directory
            shutil.copyfile(state.output_fpath, bdevperf_output_path)

    except Exception as exc:
        log.error(f"Something failed({exc})")
        log.error("".join(traceback.format_exception(None, exc, exc.__traceback__)))
        print(
            type(exc).__name__,  # TypeError
            __file__,  # /tmp/example.py
            exc.__traceback__.tb_lineno,  # 2
        )

    return err
