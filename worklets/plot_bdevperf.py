#!/usr/bin/env python
"""
    Extract and transform bdevperf output
    =====================================

    * IOPS are 'raw' / base-unit

    NOTE: The metric-context need addition of backend-options, the options are
    semi-encoded by ioengine and 'label', however, that is not very precise.
"""
import errno
import hashlib
import json
import logging as log
import os
import pprint
import re
import traceback
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from cijoe.core.analyser import to_base_unit
from cijoe.core.resources import dict_from_yamlfile
from cijoe.fio.wrapper import dict_from_fio_output_file

BDEVPERF_OUTPUT_NORMALIZED_FILENAME = "bdevperf-output-normalized.json"
BDEVPERF_OUTPUT_PREFIX = "bdevperf-output_"
JSON_DUMP = {"indent": 4}
OUTPUT_REGEX = r".*BS=(?P<bs>.*)_IODEPTH=(?P<iodepth>\d+)_LABEL=(?P<label>.*)_\d+.txt"
LINE_REGEX = r".*Total\s+\:\s+(?P<iops>\d+\.\d+)\s+IOPS\s+(?P<bwps>\d+\.\d+)\sMiB\/s.*"


def extract(args, cijoe, step):
    """
    Traverse 'args.output' for 'bdevperf-output_*.txt' files, and create:

    * A 'bdevperf-output_*.json' per 'bdevperf-output_*.txt'
    * A single "compound" 'bdevperf-output-compound.json' containing all the discovered
      JSON-documents with the file.stem as key.
    """

    search = step.get("with", {}).get("path", args.output)
    if not search:
        return errno.EINVAL

    collection = []

    search = Path(search)
    for path in search.rglob(f"{BDEVPERF_OUTPUT_PREFIX}*.txt"):
        with path.open() as ofile:
            match = re.match(OUTPUT_REGEX, str(path))

            sample = {
                "ctx": {},
                "iops": 0,
                "bwps": 0,
                "lat": 0,
                "stddev": 0,
            }

            for ctx in ["bs", "iodepth", "label"]:
                sample["ctx"][ctx] = match.group(ctx)
            sample["ctx"]["name"] = sample["ctx"]["label"]

            for line in ofile.readlines():
                metrics = re.match(LINE_REGEX, line)
                if metrics:
                    for metric in ["iops", "bwps"]:
                        sample[metric] = metrics.group(metric)

            m = hashlib.md5()
            m.update(
                str.encode(
                    "".join(
                        [
                            f"{key}={val}"
                            for key, val in sorted(sample.items())
                            if key not in ["timestamp", "stem", "iodepth"]
                        ]
                    )
                )
            )

            collection.append((str(m.hexdigest()), sample))

    artifacts = Path(args.output) / "artifacts"

    with (artifacts / BDEVPERF_OUTPUT_NORMALIZED_FILENAME).open("w") as jfd:
        json.dump(collection, jfd, **JSON_DUMP)

    return 0


def worklet_entry(args, cijoe, step):

    try:
        search = step.get("with", {}).get("path", args.output)
        if not search:
            return errno.EINVAL

        for func in [extract]:
            err = func(args, cijoe, step)
            if err:
                return err
    except Exception as exc:
        log.error(f"Something failed({exc})")
        log.error("".join(traceback.format_exception(None, exc, exc.__traceback__)))
        print(
            type(exc).__name__,  # TypeError
            __file__,  # /tmp/example.py
            exc.__traceback__.tb_lineno,  # 2
        )

    return 0
