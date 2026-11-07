def calcrc(buf, lbuf):
    ch = 0xFF
    cl = 0xFF

    for i in range(lbuf + 1):
        cl ^= buf[i]

        for _ in range(8):
            carryh = ch % 2
            carryl = cl % 2
            ch //= 2
            cl = (128 * carryh) + (cl // 2)

            if carryl:
                ch ^= 0xA0
                cl ^= 0x01

    return ch, cl


def parse_packet(raw):
    """Parse exactly eight hexadecimal bytes: six data bytes and two CRC bytes."""
    tokens = raw.split()
    if len(tokens) != 8:
        raise ValueError("Expected exactly 8 hexadecimal bytes (6 data bytes + 2 CRC bytes).")

    try:
        packet = [int(token, 16) for token in tokens]
    except ValueError as exc:
        raise ValueError("Every packet value must be a hexadecimal byte.") from exc

    if any(value < 0 or value > 0xFF for value in packet):
        raise ValueError("Each packet value must be between 00 and FF.")

    return packet


def verify_packet(packet):
    """Return validity and calculated CRC bytes for a six-byte Modbus-style frame.

    calcrc() returns the high byte then the low byte, while the packet carries
    the Modbus CRC low byte first.
    """
    if len(packet) != 8:
        raise ValueError("Expected exactly 8 bytes (6 data bytes + 2 CRC bytes).")
    if any(not isinstance(value, int) or value < 0 or value > 0xFF for value in packet):
        raise ValueError("Packet values must be integers between 00 and FF.")

    packet = list(packet)
    crc_high, crc_low = calcrc(packet[:6], 5)
    received_crc = packet[6:8]
    return received_crc == [crc_low, crc_high], crc_high, crc_low


def main():
    try:
        packet = parse_packet(input(
            "Enter the 8-byte packet in hexadecimal "
            "(e.g., A1 03 00 00 00 0F 1D 6E): "
        ))
    except ValueError as error:
        print(f"Invalid packet: {error}")
        return 2

    valid, crc_high, crc_low = verify_packet(packet)
    data = packet[:6]
    received_crc = packet[6:8]

    print(f"Packet: {' '.join(f'{value:02X}' for value in packet)}")
    print(f"Data: {data}")
    print(f"Received CRC (low byte first): {received_crc[0]:02X} {received_crc[1]:02X}")
    print(f"Calculated CRC: high={crc_high:02X}, low={crc_low:02X}")

    if valid:
        print("Data is Intact")
        return 0

    print("Data is varied!")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
