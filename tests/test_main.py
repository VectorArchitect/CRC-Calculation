import unittest
from unittest.mock import patch

from main import calcrc, main, parse_packet, verify_packet


class PacketParsingTests(unittest.TestCase):
    def test_parses_example_packet(self):
        self.assertEqual(
            parse_packet("A1 03 00 00 00 0F 1D 6E"),
            [0xA1, 0x03, 0x00, 0x00, 0x00, 0x0F, 0x1D, 0x6E],
        )

    def test_rejects_too_few_bytes(self):
        with self.assertRaisesRegex(ValueError, "exactly 8"):
            parse_packet("A1 03 00 00 00 0F 1D")

    def test_rejects_too_many_bytes(self):
        with self.assertRaisesRegex(ValueError, "exactly 8"):
            parse_packet("A1 03 00 00 00 0F 1D 6E 00")

    def test_rejects_non_hexadecimal_values(self):
        with self.assertRaisesRegex(ValueError, "hexadecimal byte"):
            parse_packet("A1 03 00 00 00 0F GG 6E")

    def test_rejects_values_outside_byte_range(self):
        with self.assertRaisesRegex(ValueError, "between 00 and FF"):
            parse_packet("A1 03 00 00 00 0F 100 6E")


class CrcVerificationTests(unittest.TestCase):
    def test_calculates_documented_crc_vector(self):
        self.assertEqual(calcrc([0xA1, 0x03, 0, 0, 0, 0x0F], 5), (0x6E, 0x1D))

    def test_accepts_modbus_low_byte_first_packet(self):
        valid, crc_high, crc_low = verify_packet(
            [0xA1, 0x03, 0, 0, 0, 0x0F, 0x1D, 0x6E]
        )
        self.assertTrue(valid)
        self.assertEqual((crc_high, crc_low), (0x6E, 0x1D))

    def test_accepts_bytes_input(self):
        packet = bytes([0xA1, 0x03, 0, 0, 0, 0x0F, 0x1D, 0x6E])
        self.assertTrue(verify_packet(packet)[0])

    def test_rejects_corrupted_crc(self):
        valid, _, _ = verify_packet([0xA1, 0x03, 0, 0, 0, 0x0F, 0x1D, 0x00])
        self.assertFalse(valid)

    def test_main_reports_example_packet_as_intact(self):
        with patch("builtins.input", return_value="A1 03 00 00 00 0F 1D 6E"):
            with patch("builtins.print") as mock_print:
                self.assertEqual(main(), 0)
        output = " ".join(str(call.args[0]) for call in mock_print.call_args_list)
        self.assertIn("Data is Intact", output)

    def test_main_returns_error_for_invalid_input(self):
        with patch("builtins.input", return_value="A1 03"):
            with patch("builtins.print") as mock_print:
                self.assertEqual(main(), 2)
        self.assertIn("Invalid packet", mock_print.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
