# Pebble Console Specification

Version: 1.0

---

# CPU

- W65C02
- Clock: 1 MHz

---

# Memory

## RAM

8 KB total

| Address | Description |
|----------|-------------|
| $0000-$03FF | 1 KB Video Framebuffer |
| $0400-$1FEF | General Purpose RAM |
| $1FF0-$1FFF | Hardware Registers |

## ROM

| Address | Description |
|----------|-------------|
| $8000-$FFFF | 32 KB Cartridge ROM |

---

# Video

Resolution:

64 × 64 pixels

Color Depth:

2 bits per pixel

Palette:

00 = White

01 = Light Gray

10 = Dark Gray

11 = Black

Refresh Rate:

30 Hz

---

# Controller

Buttons:

- Up
- Down
- Left
- Right
- A
- B
- Start

Controller Register:

$1FF0

Bit Layout:

Bit 0 = Up

Bit 1 = Down

Bit 2 = Left

Bit 3 = Right

Bit 4 = A

Bit 5 = B

Bit 6 = Start

Bit 7 = Reserved

---

# Hardware Registers

| Address | Purpose |
|----------|----------|
| $1FF0 | Controller |
| $1FF1 | Frame Counter |
| $1FF2 | Random Number |
| $1FF3 | Video Status |
| $1FF4-$1FFF | Reserved |

---

# Video Status Register

$1FF3

Bit 0

0 = Drawing

1 = VBlank

---

# Cartridge

- Fixed Size
- 32 KB
- Raw binary
- No bank switching
- No mapper

---

# Graphics

Software-rendered.

No hardware sprites.

No hardware tiles.

No hardware scrolling.

All drawing is performed by the CPU.