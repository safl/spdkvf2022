#!/usr/bin/env python3

devices = {
    "gen4": [
        {"pcie": "0000:05:00.0", "label": "M10_16GB"},
        {"pcie": "0000:07:00.0", "label": "M10_16GB"},
        {"pcie": "0000:01:00.0", "label": "M10_16GB"},

        {"pcie": "0000:09:00.0", "label": "980PRO_512GB"},
        {"pcie": "0000:0a:00.0", "label": "980PRO_1TB"},
        {"pcie": "0000:02:00.0", "label": "980PRO_1TB"},
        {"pcie": "0000:03:00.0", "label": "980PRO_1TB"},
    ]

    "gen3": [
        {"pcie": "0000:41:00.0", "os": "nvme0n1", "label": "M10_16GB"},
        {"pcie": "0000:42:00.0", "os": "nvme1n1", "label": "M10_16GB"},
        {"pcie": "0000:43:00.0", "os": "nvme2n1", "label": "M10_16GB"},
        {"pcie": "0000:44:00.0", "os": "nvme3n1", "label": "M10_16GB"},

        {"pcie": "0000:45:00.0", "os": "nvme4n1", "label": "980PRO_2TB"},
        {"pcie": "0000:46:00.0", "os": "nvme5n1", "label": "980PRO_2TB"},
        {"pcie": "0000:47:00.0", "os": "nvme6n1", "label": "980PRO_2TB"},
        {"pcie": "0000:48:00.0", "os": "nvme7n1", "label": "980PRO_2TB"},
    ]
}


def main():
    print("hello")


if __name__ == "__main__":
    main()
