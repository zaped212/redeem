from unittest import TestCase

import sys
sys.path.insert(0, '../redeem')

from Gcode import Gcode
from mock import patch, Mock

class Printer():
    factor = 1.0

class GcodeTest(TestCase):

    def setUp(self):
        Gcode.printer = Printer()
        packet = {
            "message": "N99  G2 8 x0 Y-0.2345 z +12.345 67 ab C(comment)*92; noise",
            "answer": "ok"
            }
        self.g = Gcode(packet)

    def tearDown(self):
        self.g = None
        return

    def test_gcode_parser(self): # Gocde::__init__
        self.assertEqual(self.g.gcode, "G28")
        self.assertEqual(self.g.tokens, ["X0", "Y-0.2345", "Z+12.34567", "A", "B", "C"])

        packet = {"message": "; noise"}
        g = Gcode(packet)
        self.assertEqual(g.code(), "No-Gcode")

    def test_gcode_code(self):
        self.assertEqual(self.g.code(), "G28")

    def test_gcode_is_valid(self):
        self.assertEqual(self.g.is_valid(), True)

        packet = {"message": "N99  G28*60; noise"} # invalid checksum
        g = Gcode(packet)
        self.assertEqual(g.is_valid(), False)

    def test_gcode_token_letter(self):
        self.assertEqual(self.g.token_letter(2), "Z")

    def test_token_value(self):
        self.assertEqual(self.g.token_value(1), -0.2345)

    def test_gcode_token_distance(self):
        self.assertEqual(self.g.token_distance(2), 12.34567)

        t = self.g.printer.factor
        self.g.printer.factor = 2.54
        self.assertEqual(self.g.token_distance(2), 12.34567 * 2.54)
        self.g.printer.factor = t

    def test_gcode_get_tokens(self):
        self.assertEqual(self.g.get_tokens(), self.g.tokens)

    def test_gcode_set_tokens(self):
        g = Gcode({"message": "G28"})
        g.set_tokens(["G28", "X0", "Y0"])
        self.assertEqual(g.tokens, ["G28", "X0", "Y0"])

    def test_gcode_get_message(self):
        """ should return message with line number, checksum, gcode (comments) and non-standrd ;comments removed """
        self.assertEqual(self.g.get_message(), "G2 8 x0 Y-0.2345 z +12.345 67 ab C")

    def test_gcode_has_letter(self):
        self.assertEqual(self.g.has_letter("Y"), True)
        self.assertEqual(self.g.has_letter("W"), False)
        self.assertEqual(self.g.has_letter("N"), False)
        self.assertEqual(self.g.has_letter("W"), False)
        self.assertEqual(self.g.has_letter("B"), True)
        self.assertEqual(self.g.has_letter("C"), True)

    def test_gcode_has_value(self):
        self.assertEqual(self.g.has_value(0), True)
        self.assertEqual(self.g.has_value(1), True)
        self.assertEqual(self.g.has_value(2), True)
        self.assertEqual(self.g.has_value(3), False)
        self.assertEqual(self.g.has_value(4), False)
        self.assertEqual(self.g.has_value(5), False)

    def test_gcode_get_token_index_by_letter(self):
        self.assertEqual(self.g.get_token_index_by_letter("X"), 0)
        self.assertEqual(self.g.get_token_index_by_letter("Y"), 1)
        self.assertEqual(self.g.get_token_index_by_letter("C"), 5)

    def test_gcode_get_float_by_letter(self):
        self.assertEqual(self.g.get_float_by_letter("Y"), -0.2345)

    def test_gcode_get_distance_by_letter(self):
        t = self.g.printer.factor
        self.g.printer.factor = 2.54
        self.assertEqual(self.g.get_distance_by_letter("Y"), -0.2345 * 2.54)
        self.g.printer.factor = t

    def test_gcode_get_int_by_letter(self):
        self.assertEqual(self.g.get_int_by_letter("Z"), 12)

    def test_gcode_has_letter_value(self):
        self.assertEqual(self.g.has_letter_value("X"), True)
        self.assertEqual(self.g.has_letter_value("A"), False)

    def test_gcode_remove_token_by_letter(self):
        t = self.g
        self.g.remove_token_by_letter("Z")
        self.assertEqual(self.g.tokens, ["X0", "Y-0.2345", "A", "B", "C"])
        self.g = t

    def test_gcode_num_tokens(self):
        self.assertEqual(self.g.num_tokens(), 6)

    def test_gcode_get_tokens_as_dict(self):
        t = self.g.get_tokens_as_dict()
        keys = ["A", "B", "C", "X", "Y", "Z"]
        vals = [0.0, 0.0, 0.0, 0.0, -0.2345, 12.34567]
        for i, key in enumerate(sorted(t)):
            self.assertEqual(key, keys[i])
            self.assertEqual(t[key], vals[i])

    def test_gcode__get_cs(self):
        self.assertEqual(1, self.g._getCS("1234567890"))

    def test_gcode_is_crc(self):
        self.assertEqual(self.g.is_crc(), True)
        g = Gcode({"message": "G28"})
        self.assertEqual(g.is_crc(), False)

    def test_gcode_get_answer(self):
        self.assertEqual(self.g.get_answer(), "ok")

    def test_gcode_set_answer(self):
        t = self.g.answer
        self.assertEqual(self.g.answer, "ok")
        self.g.set_answer("xxx")
        self.assertEqual(self.g.answer, "xxx")
        self.g.answer = t

    def test_gcode_is_info_command(self):
        self.assertEqual(self.g.is_info_command(), False)
        g = Gcode({"message": "G28?"})
        self.assertEqual(g.is_info_command(), True)

