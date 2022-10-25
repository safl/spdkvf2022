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


def worklet_entry(args, cijoe, step):

    repetitions = step.get("with", {}).get("repetitions", 3)
    iosizes = step.get("with", {}).get("iosizes", ["4K"])
    iodepths = step.get("with", {}).get("iodepths", [1, 2, 4, 8])

    cdev = {"uri": "/dev/ng0n1", "nsid": 1, "labels": ["cdev"]}
    bdev = {"uri": "/dev/nvme0n1", "nsid": 1, "labels": ["bdev"]}
    pcie = {"uri": "0000:01:00.0", "nsid": 1, "labels": ["pcie"]}

    implementation = {
        "io_uring_cmd-bdev_xnvme": {
            "engine": "spdk_bdev",
            "device": cdev,
            "xnvme_opts": {},
            "spdk_opts": {
                "bdev": "xnvme",
                "params": {
                    "filename": cdev["uri"],
                    "name": "Nvme0n1",
                    "io_mechanism": "io_uring_cmd",
                    # "conserve_cpu": False,
                    # "conserve_cpu": True,
                },
            },
        },
        "io_uring-bdev_uring": {
            "engine": "spdk_bdev",
            "device": bdev,
            "xnvme_opts": {},
            "spdk_opts": {
                "bdev": "uring",
                "params": {"filename": bdev["uri"], "name": "Nvme0n1"},
            },
        },
        "io_uring-bdev_xnvme": {
            "engine": "spdk_bdev",
            "device": bdev,
            "xnvme_opts": {},
            "spdk_opts": {
                "bdev": "xnvme",
                "params": {
                    "filename": bdev["uri"],
                    "name": "Nvme0n1",
                    "io_mechanism": "io_uring",
                    # "conserve_cpu": False,
                    # "conserve_cpu": True,
                },
            },
        },
        "libaio-bdev_aio": {
            "engine": "spdk_bdev",
            "device": bdev,
            "xnvme_opts": {},
            "spdk_opts": {
                "bdev": "aio",
                "params": {"filename": bdev["uri"], "name": "Nvme0n1"},
            },
        },
        "libaio-bdev_xnvme": {
            "engine": "spdk_bdev",
            "device": bdev,
            "xnvme_opts": {},
            "spdk_opts": {
                "bdev": "xnvme",
                "params": {
                    "filename": bdev["uri"],
                    "name": "Nvme0n1",
                    "io_mechanism": "libaio",
                    # "conserve_cpu": False,
                    # "conserve_cpu": True,
                },
            },
        },
    }

    artifacts = Path(args.output) / "artifacts"
    os.makedirs(str(artifacts), exist_ok=True)

    err = 0
    try:
        for (bs, iodepth, (label, params), rep) in product(
            iosizes, iodepths, implementation.items(), range(repetitions)
        ):
            bdevperf_output_path = (
                artifacts
                / f"bdevperf-output_BS={bs}_IODEPTH={iodepth}_LABEL={label}_{rep}.txt"
            )

            # Create a spdk-configuration file and transfer it
            stem, spdk_conf_path, conf = spdk_opts_to_spdk_conf(
                params["spdk_opts"], "/tmp"
            )
            cijoe.run(f"rm {spdk_conf_path} || true")
            cijoe.put(spdk_conf_path, spdk_conf_path)

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
