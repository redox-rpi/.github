## Redox OS on the Raspberry Pi

We bring [Redox OS](https://www.redox-os.org/), the microkernel operating
system written in Rust, to the **Raspberry Pi 3B+** and the **Raspberry Pi
Zero 2 W**, as a small headless server. Both boards share the same SoC
family, so one kernel and one driver set cover them.

### Status

Latest release: [v0.2.0](https://github.com/redox-rpi/redox-rpi/releases/latest),
experimental (alpha), not for daily use.

| | State |
|---|---|
| Real Pi 3B+: all 4 cores, boot from SD card or over the network | ✅ |
| USB keyboard and HDMI console (own DWC2 USB driver) | ✅ plugged in before boot; hotplug planned |
| Ethernet: LAN7800 on the Pi 3B+, RTL8152/RTL8153 on the Zero 2 W HAT | ✅ |
| Time over NTP at boot | ✅ |
| Zero 2 W | ✅ boots the Pi 3B+ image |
| Random start crashes | 🟡 main cause fixed, one rare crash left |
| Faster SD card driver (sdhost), full CPU speed | 🟡 planned for v0.3.0 |

Details: [roadmap](https://github.com/redox-rpi/redox-rpi/blob/main/ROADMAP.md) ·
[topics](https://github.com/redox-rpi/redox-rpi/blob/main/docs/topics/README.md) ·
[known issues](https://github.com/redox-rpi/redox-rpi/blob/main/docs/known-issues.md)

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

All tasks, bugs and plans are tracked in **one place**: the
[issues of redox-rpi/redox-rpi](https://github.com/redox-rpi/redox-rpi/issues),
also for the other repositories here (such as
[relibc](https://github.com/redox-rpi/relibc)).

- **Labels:** `topic:…` for the area (stability, sdcard, usb, network,
  firmware, boot, …), `needs:pi`, `needs:qemu`, `needs:zero2w` or
  `needs:nothing` for the hardware you need, `in-progress` while someone
  works on it. Tasks without hardware: [needs:nothing](https://github.com/redox-rpi/redox-rpi/issues?q=is%3Aopen+label%3Aneeds%3Anothing),
  in QEMU: [needs:qemu](https://github.com/redox-rpi/redox-rpi/issues?q=is%3Aopen+label%3Aneeds%3Aqemu).
- **Releases** are milestones, for example
  [v0.3.0](https://github.com/redox-rpi/redox-rpi/milestone/1).
- **Topic pages** in [docs/topics/](https://github.com/redox-rpi/redox-rpi/blob/main/docs/topics/README.md)
  say what works, what is in progress and what comes next.
- **The same rules for everyone**, people and AI agents: say in the issue
  that you take it, comment as you go in short, plain English, and open a
  pull request that names the issue. Only maintainers merge. Details in
  [CONTRIBUTING.md](https://github.com/redox-rpi/redox-rpi/blob/main/CONTRIBUTING.md).
- Questions and ideas: [Discussions](https://github.com/redox-rpi/redox-rpi/discussions).

### About this project

This is an **unofficial fork** and not part of the Redox OS project. It is
developed with the help of AI coding tools, which Redox does not accept
upstream, so please report problems here and not to Redox. Everything is
MIT-licensed like Redox itself.

Help is welcome, especially from people with a Pi 3B+, a Zero 2 W and a
serial adapter on their desk.

Idea in progress: an [AI challenge](https://github.com/redox-rpi/redox-rpi/blob/main/docs/ai-challenge.md)
to port an OS to the Pi (draft, comments welcome in
[Discussions](https://github.com/redox-rpi/redox-rpi/discussions)).
