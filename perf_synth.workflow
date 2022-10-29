---
doc: |
  Run the one-core-peak.sh and variations

steps:
- name: t_io_uring_nvme_default
  uses: t_io_uring
  with:
    mode: default
    io_mechanism: io_uring

- name: t_io_uring_nvme_n1
  uses: t_io_uring
  with:
    mode: tweak_n1
    io_mechanism: io_uring

- name: t_io_uring_nvme_n2
  uses: t_io_uring
  with:
    mode: tweak_n2
    io_mechanism: io_uring

- name: t_io_uring_nvme_n2_batch
  uses: t_io_uring
  with:
    mode: tweak_n2_batch
    io_mechanism: io_uring

- name: t_io_uring_cmd_nvme_default
  uses: t_io_uring
  with:
    mode: default
    io_mechanism: io_uring_cmd

- name: t_io_uring_cmd_nvme_n1
  uses: t_io_uring
  with:
    mode: tweak_n1
    io_mechanism: io_uring_cmd

- name: t_io_uring_cmd_nvme_n2
  uses: t_io_uring
  with:
    mode: tweak_n2
    io_mechanism: io_uring_cmd

- name: t_io_uring_cmd_nvme_n2_batch
  uses: t_io_uring
  with:
    mode: tweak_n2_batch
    io_mechanism: io_uring_cmd
