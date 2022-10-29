---
doc: |
  Run the one-core-peak.sh and variations

steps:
- name: block_default
  uses: t_io_uring
  with:
    mode: default
    io_mechanism: io_uring

- name: block_thread1
  uses: t_io_uring
  with:
    mode: tweak_n1
    io_mechanism: io_uring

- name: block_thread2
  uses: t_io_uring
  with:
    mode: tweak_n2
    io_mechanism: io_uring

- name: block_n2batch
  uses: t_io_uring
  with:
    mode: tweak_n2_batch
    io_mechanism: io_uring

- name: chard_default
  uses: t_io_uring
  with:
    mode: default
    io_mechanism: io_uring_cmd

- name: chard_thread1
  uses: t_io_uring
  with:
    mode: tweak_n1
    io_mechanism: io_uring_cmd

- name: chard_thread2
  uses: t_io_uring
  with:
    mode: tweak_n2
    io_mechanism: io_uring_cmd

- name: chard_n2batch
  uses: t_io_uring
  with:
    mode: tweak_n2_batch
    io_mechanism: io_uring_cmd
