## Redox OS on the Raspberry Pi

We bring [Redox OS](https://www.redox-os.org/), the microkernel operating
system written in Rust, to the **Raspberry Pi 3** and the **Raspberry Pi
Zero 2 W**, as a small headless server. Both boards share the same SoC
family, so one kernel and one driver set cover them.

### Status

| Step | State |
|---|---|
| Boots in QEMU's emulated Pi 3 (`raspi3b`) to a root shell | ✅ with a devicetree fix from this project |
| Userspace programs in today's daily image | 🟡 upstream regression, being tracked |
| All 4 CPU cores (spin-table, BCM2836 IPIs) | ✅ in QEMU |
| Real Pi 3B+: network boot to the login prompt | ✅ 2026-10-25 |
| Login on real hardware (serial console, USB keyboard) | ⏳ next |
| Zero 2 W board variant | ⏳ planned |
| Ethernet (DWC2 USB host, Pi 3 onboard and Zero 2 W HATs) | ⏳ planned |

Details: [status and findings](https://github.com/redox-rpi/redox-rpi/blob/main/docs/status.md) ·
[roadmap](https://github.com/redox-rpi/redox-rpi/blob/main/ROADMAP.md)

### Try it

On macOS or Linux with QEMU, curl and zstd:

```sh
git clone https://github.com/redox-rpi/redox-rpi.git
cd redox-rpi
scripts/qemu-raspi3b.sh
```

### About this project

This is an **unofficial fork** and not part of the Redox OS project. It is
developed with the help of AI coding tools, which Redox does not accept
upstream, so please report problems here and not to Redox. Everything is
MIT-licensed like Redox itself.

Issues, ideas and pull requests are welcome, especially from people with a
Pi 3, a Zero 2 W and a serial adapter on their desk.

Idea in progress: an [AI challenge](https://github.com/redox-rpi/redox-rpi/blob/main/docs/ai-challenge.md)
to port an OS to the Pi (draft, comments welcome in
[Discussions](https://github.com/redox-rpi/redox-rpi/discussions)).
