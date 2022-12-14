---
doc: |
  Run the one-core-peak.sh and variations

steps:
- name: block_default
  uses: t_io_uring
  with:
    mode: default
    io_mechanism: io_uring
    bin: /opt/t_io_uring/io_uring

#- name: block_thread1
#  uses: t_io_uring
#  with:
#    mode: tweak_n1
#    io_mechanism: io_uring
#    bin: /opt/t_io_uring/io_uring

#- name: block_thread2
#  uses: t_io_uring
#  with:
#    mode: tweak_n2
#    io_mechanism: io_uring
#    bin: /opt/t_io_uring/io_uring

- name: block_n2batch
  uses: t_io_uring
  with:
    mode: tweak_n2_batch
    io_mechanism: io_uring
    bin: /opt/t_io_uring/io_uring

- name: block_n2_nopoll
  uses: t_io_uring
  with:
    mode: tweak_n2_nopoll
    io_mechanism: io_uring
    bin: /opt/t_io_uring/io_uring

- name: block_n2_nopnob
  uses: t_io_uring
  with:
    mode: tweak_n2_nopnob
    io_mechanism: io_uring
    bin: /opt/t_io_uring/io_uring

- name: block_n1_sqpoll
  uses: t_io_uring
  with:
    mode: tweak_n1_sqpoll
    io_mechanism: io_uring_cmd
    bin: /opt/t_io_uring/io_uring_sqpoll



- name: chard_default
  uses: t_io_uring
  with:
    mode: default
    io_mechanism: io_uring_cmd
    bin: /opt/t_io_uring/io_uring

#- name: chard_thread1
#  uses: t_io_uring
#  with:
#    mode: tweak_n1
#    io_mechanism: io_uring_cmd
#    bin: /opt/t_io_uring/io_uring

#- name: chard_thread2
#  uses: t_io_uring
#  with:
#    mode: tweak_n2
#    io_mechanism: io_uring_cmd
#    bin: /opt/t_io_uring/io_uring

- name: chard_n2batch
  uses: t_io_uring
  with:
    mode: tweak_n2_batch
    io_mechanism: io_uring_cmd
    bin: /opt/t_io_uring/io_uring

- name: chard_n2_nopoll
  uses: t_io_uring
  with:
    mode: tweak_n2_nopoll
    io_mechanism: io_uring_cmd
    bin: /opt/t_io_uring/io_uring

- name: chard_n2_nopnob
  uses: t_io_uring
  with:
    mode: tweak_n2_nopnob
    io_mechanism: io_uring_cmd
    bin: /opt/t_io_uring/io_uring

- name: chard_n1_sqpoll
  uses: t_io_uring
  with:
    mode: tweak_n1_sqpoll
    io_mechanism: io_uring_cmd
    bin: /opt/t_io_uring/io_uring_sqpoll
