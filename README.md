# CRC-Calculation

A small Python command-line utility for checking an eight-byte CRC-16 packet.

## Packet format

The example frame contains six data bytes followed by a two-byte CRC:

```text
A1 03 00 00 00 0F 1D 6E
```

The calculation uses the existing CRC-16 algorithm with polynomial `0xA001` and initial value `0xFFFF`. The calculation helper returns the CRC high byte and low byte separately; the packet example uses Modbus wire order, which transmits the low byte first (`1D 6E`).

The checker now requires exactly eight hexadecimal byte values, rejects malformed or out-of-range input, and compares the received CRC in low-byte-first order.

## Run

Requires Python 3.8 or newer. No third-party packages are needed.

```bash
python main.py
```

## Tests

Run the standard-library test suite from the repository root:

```bash
python -m unittest discover -s tests -v
```

The tests cover the documented CRC vector, packet parsing, byte order, corrupted CRCs, and command-line error handling.
