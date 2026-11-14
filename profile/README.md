## Redox OS on the Raspberry Pi

We bring [Redox OS](https://www.redox-os.org/), the microkernel operating
system written in Rust, to the Raspberry Pi.

**Vision:** Redox runs on (almost) every Raspberry Pi from the Zero 2 W
upwards, from a small headless server to a desktop with a screen, keyboard
and mouse. We started with the boards that share one SoC family (Pi 3B+ and
Zero 2 W) and add the newer ones step by step.

### Boards

| Board | SoC | State |
|---|---|---|
| Raspberry Pi 3B+ | BCM2837B0, 4× Cortex-A53 | ✅ main test board, every release is tested on it |
| Raspberry Pi Zero 2 W | RP3A0 (BCM2710A1), 4× Cortex-A53 | ✅ boots the Pi 3B+ image; network through a USB Ethernet HAT |
| Raspberry Pi 3B, 3A+ | BCM2837 | 🟡 same SoC family, expected to work, not tested |
| Raspberry Pi 4, 400, CM4 | BCM2711, 4× Cortex-A72 | 🔜 next board family: new interrupt controller, PCIe, GENET Ethernet |
| Raspberry Pi 5, 500, CM5 | BCM2712 + RP1 | 🔜 after the Pi 4 |
| Pi 1, 2, Zero, Zero W, Pico | 32-bit or microcontroller | ❌ out of scope: Redox needs a 64-bit CPU with an MMU |

### Where we are

Latest release: [v0.4.0](https://github.com/redox-rpi/redox-rpi/releases/latest)
(2026-11-09), experimental (alpha), not for daily use. New in v0.4.0: an
optional desktop, sound from the headphone jack, fast small writes to the
SD card, every network adapter at once. We release every week.

| Area | State |
|---|---|
| Boot from SD card or over the network, all 4 cores, boot menu | ✅ |
| Programs start reliably (0 of 1000 starts failed in the v0.4.0 test) | ✅ |
| Console on HDMI and on the serial port, USB keyboard and mouse, hotplug | ✅ |
| Ethernet (LAN7800 on the 3B+, RTL8152/8153 on the Zero 2 W HAT), every adapter at once | ✅ |
| SD card (own sdhost driver), RedoxFS read and write | ✅ |
| CPU clock follows the load (600 to 1400 MHz), time over NTP | ✅ |
| GPIO, I2C and SPI on the pin header | ✅ first versions |
| Sound on the headphone jack (PWM, 44.1 kHz) | 🧪 beta since v0.4.0 |
| Optional desktop (Orbital with COSMIC apps), started from the console with `desktop` | 🧪 beta since v0.4.0 |
| Native C compiler on the Pi (TinyCC) | 🧪 experiment, in the image with the next release |
| Own display driver (VC4 HVS, [vc4d](https://github.com/redox-rpi/vc4d)) | 🚧 in progress |
| Open-source boot firmware ([rpi-open-firmware](https://github.com/redox-rpi/rpi-open-firmware)) | 🚧 experiment |
| Wi-Fi, IPv6 | 🔜 planned for v0.6.0 |
| SSH and prebuilt programs | 🔜 planned for v0.7.0 |

Details: [roadmap](https://github.com/redox-rpi/redox-rpi/blob/main/ROADMAP.md) ·
[topics](https://github.com/redox-rpi/redox-rpi/blob/main/docs/topics/README.md) ·
[known issues](https://github.com/redox-rpi/redox-rpi/blob/main/docs/known-issues.md)

### How it fits together

```
 Raspberry Pi firmware (bootcode.bin, start.elf)   or   rpi-open-firmware (experiment)
        │
 U-Boot with a boot menu: SD card or network boot
        │
 Redox bootloader  →  Redox microkernel (aarch64, patched for the BCM2837)
        │
 Drivers run as normal programs in user space, each its own process:
   USB (dwc2d) · SD card (sdhost) · Ethernet · framebuffer (rpi-fbd)
   GPIO / I2C / SPI · PWM audio · CPU clock · time (NTP)
        │
 relibc (Redox's C library) · netstack · RedoxFS
        │
 Shell (Ion), core tools, optional desktop (Orbital + COSMIC apps), TinyCC
```

Everything above the firmware is open source. We follow upstream Redox:
our changes are small patches on top of a pinned upstream version
(`upstream.lock`), so every image can be rebuilt exactly.

### The VideoCore IV part

Besides the four ARM cores, every Pi 3B+ and Zero 2 W has a VideoCore IV
(VC4). It has two halves:
- the **VPU**, a separate processor that starts first and runs the boot
  firmware (`bootcode.bin`, `start.elf`)
- the **GPU** with the display pipeline (HVS) and 3D

The Raspberry Pi firmware for it is closed. We work on it from both sides:

- **ARM side, the display:** [vc4d](https://github.com/redox-rpi/vc4d) is a
  Redox driver that drives the HVS and later 3D directly, instead of the
  firmware's simple framebuffer. It is ported from Linux vc4.
- **VPU side, the firmware:**
  [rpi-open-firmware](https://github.com/redox-rpi/rpi-open-firmware) is an
  open-source `bootcode.bin` that brings up the RAM and loads the next stage.
  The experiment boots on the 3B+.
- **Tools for the VPU:**
  - [tinycc](https://github.com/redox-rpi/tinycc) is our TinyCC with a VC4
    backend, so the firmware can be built with a small compiler of our own,
    without the old vc4-elf GCC. The same TinyCC is the C compiler on the Pi.
  - [resim](https://github.com/redox-rpi/resim) is a VC4 simulator, so
    compiler and firmware can be tested without a Pi. A weekly run compiles
    1,000 random programs (csmith) with both compilers and compares the
    results in the simulator.
  - [vc4-toolchain](https://github.com/redox-rpi/vc4-toolchain) pins every
    one of these tools to an exact commit and has the scripts that build and
    test them.

All of this is experimental. Releases still boot with the Raspberry Pi
firmware.

### Repositories

| Repository | What |
|---|---|
| [redox-rpi](https://github.com/redox-rpi/redox-rpi) | build, patches against upstream Redox, image configuration, releases, docs |
| [relibc](https://github.com/redox-rpi/relibc) | our fork of Redox's C library with the aarch64 fixes |
| [pi-tests](https://github.com/redox-rpi/pi-tests) | test queue, test reports and evidence from the real Pis |
| [vc4d](https://github.com/redox-rpi/vc4d) | display driver for the VideoCore IV (in progress, GPL-2.0) |
| [rpi-open-firmware](https://github.com/redox-rpi/rpi-open-firmware) | open-source boot firmware for the VPU (experiment) |
| [tinycc](https://github.com/redox-rpi/tinycc) | TinyCC for Redox on the Pi, with a VC4 backend (LGPL-2.1) |
| [resim](https://github.com/redox-rpi/resim) | VideoCore IV simulator for testing without a Pi |
| [vc4-toolchain](https://github.com/redox-rpi/vc4-toolchain) | pinned versions and build and test scripts of the VC4 tools |

### Try it

Flash the image of the [latest release](https://github.com/redox-rpi/redox-rpi/releases/latest)
to a microSD card (Raspberry Pi Imager "Use custom", balenaEtcher or `dd`)
and boot a Pi 3B+ or a Zero 2 W with it. Without a Pi, the kernel boots in
QEMU on macOS or Linux:

```sh
git clone https://github.com/redox-rpi/redox-rpi.git
cd redox-rpi
scripts/qemu-raspi3b.sh
```

### How we work

All tasks, bugs and plans are tracked in the
[issues of redox-rpi/redox-rpi](https://github.com/redox-rpi/redox-rpi/issues).
We are moving to issues in the repository each one concerns, with the
GitHub issue types Feature, Bug and Task.

- **Labels:** `topic:…` for the area (stability, sdcard, usb, network,
  firmware, boot, …), `needs:pi`, `needs:qemu`, `needs:zero2w` or
  `needs:nothing` for the hardware you need. Tasks without hardware:
  [needs:nothing](https://github.com/redox-rpi/redox-rpi/issues?q=is%3Aopen+label%3Aneeds%3Anothing),
  in QEMU: [needs:qemu](https://github.com/redox-rpi/redox-rpi/issues?q=is%3Aopen+label%3Aneeds%3Aqemu).
- **Releases** are milestones, for example
  [v0.4.0](https://github.com/redox-rpi/redox-rpi/milestone/3).
- **Every change is tested on a real Pi** before it reaches `main`.
- **The same rules for everyone**, people and AI agents: say in the issue
  that you take it, comment as you go in short, plain English, and open a
  pull request that names the issue. Only maintainers merge. Details in
  [CONTRIBUTING.md](https://github.com/redox-rpi/redox-rpi/blob/main/CONTRIBUTING.md).
- Questions and ideas: [Discussions](https://github.com/redox-rpi/redox-rpi/discussions).
- Chat: Matrix room [#redox-rpi:matrix.org](https://matrix.to/#/#redox-rpi:matrix.org).

### About this project

This is an **unofficial fork** and not part of the Redox OS project. It is
developed by one maintainer with a team of AI coding agents, which Redox
does not accept upstream, so please report problems here and not to Redox.
Our own code is MIT-licensed like Redox itself. Forks keep the licence of
their original: vc4d is GPL-2.0 (from Linux), tinycc LGPL-2.1.

People and AI agents are welcome to join, especially with a Pi 3B+, a
Zero 2 W, a Pi 4 or a Pi 5 and a serial adapter on the desk. How to start:
[join the project](https://github.com/redox-rpi/redox-rpi/blob/main/docs/join.md).
