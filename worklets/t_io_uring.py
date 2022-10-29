PARAMS_DEFAULT = {
    "d": "128",  # <int>  IO Depth, default 128
    "s": "32",  # <int>  Batch submit, default 32
    "c": "32",  # <int>  Batch complete, default 32
    "b": "512",  # <int>  Block size, default 4096
    "p": "1",  # <bool> Polled IO, default 1
    "B": "1",  # <bool> Fixed buffers, default 1
    "D": "0",  # <bool> DMA map fixed buffers, default 0
    "F": "1",  # <bool> Register files, default 1
    "n": "1",  # <int>  Number of threads, default 1
    "O": "1",  # <bool> Use O_DIRECT, default 1
    "N": "0",  # <bool> Perform just no-op requests, default 0
    "t": "0",  # <bool> Track IO latencies, default 0
    "T": "0",  # <int>  TSC rate in HZ
    "r": "0",  # <int>  Runtime in seconds, default unlimited
    "R": "1",  # <bool> Use random IO, default 1
    "a": "0",  # <bool> Use legacy aio, default 0
    "S": "0",  # <bool> Use sync IO (preadv2), default 0
    "X": "0",  # <bool> Use registered ring 1
    "P": "0",  # <bool> Automatically place on device home node 0
    "u": "0",  # <bool> Use nvme-passthrough I/O, default 0
}

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


def worklet_entry(cijoe, args, step):

    mode = step.get("with", {}).get("mode", "default")
    io_mechanism = step.get("with", {}).get("mode", "io_mechanism")

    handles = []
    for device_info in SYSTEMS["gen4"]:
        params = PARAMS_DEFAULT.copy()

        handle = "/nvme{device_info['os']}"
        if io_mechanism == "io_uring_cmd":
            handle = "/ng{device_info['os']}"
            params["u"] = "1"
            params["O"] = "0"

        handles.append(handle)

        if mode == "default":           # Default: n threads for n devices
            params["n"] = len(handles)
        elif mode == "tweak_n1":        # Tweak: 1 thread for n devices
            params["n"] = "1"
        elif mode == "tweak_n2":        # Tweak: 2 threads for n devices
            params["n"] = "2"
        elif mode == "tweak_n2_batch":  # Tweak: 2 threads for n devices + reduce batch
            params["n"] = "2"
            params["c"] = "16"
            params["s"] = "16"

        cmd = " ".join(
            [
                "taskset -c 0,1",
                " ".join([f"-{k}{v}" for k, v in params]),
                " ".join(handles),
            ]
        )

        err, _ = cijoe.run(cmd)
