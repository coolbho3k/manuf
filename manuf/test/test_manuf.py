import manuf
import os
import unittest

class ManufTestCase(unittest.TestCase):
    MANUF_URL = "https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf"

    def setUp(self):
        self.manuf = manuf.MacParser(manuf_name="manuf")
    #
    def test_update_update(self):
        self.manuf.update(manuf_url=self.MANUF_URL, manuf_name="manuf_update")
        assert os.path.exists("manuf_update")
        os.remove("manuf_update")

    def test_getAll_whenMacValid_getVendor(self):
        v = self.manuf.get_all("00:00:00:00:00:00")
        self.assertEqual(v.manuf, "00:00:00")
        self.assertEqual(v.manuf_long, "Officially Xerox, but 0:0:0:0:0:0 is more common")

    def test_getManuf_getManuf(self):
        m = self.manuf.get_manuf("08:60:6E")
        v = self.manuf.get_all("08:60:6E")
        self.assertEqual(m, "AsustekC")
        self.assertEqual(m, v.manuf)

    def test_getManufLong_getManufLong(self):
        ml = self.manuf.get_manuf_long("08:60:6E")
        v = self.manuf.get_all("08:60:6E")
        self.assertEqual(ml, "ASUSTek COMPUTER INC.")
        self.assertEqual(ml, v.manuf_long)

    def test_getManufLong_getComment(self):
        v = self.manuf.get_all("00:20:35")
        self.assertEqual(v.manuf_long, "IBM (International Business Machines)")
        self.assertEqual(v.comment, "mainframes, Etherjet printers")

    def test_getAll_supportAllMacFormats(self):
        v1 = self.manuf.get_all("08:60:6E")
        v2 = self.manuf.get_all("08:60:6e:dd:dd:dd")
        v3 = self.manuf.get_all("08.60.6E.ab.cd.ef")
        v4 = self.manuf.get_all("08-60-6E")
        self.assertEqual(v1.manuf, "AsustekC")
        self.assertEqual(v1.manuf_long, "ASUSTek COMPUTER INC.")
        self.assertEqual(v1, v2)
        self.assertEqual(v1, v3)
        self.assertEqual(v1, v4)

    def test_getAll_returnClosestMatch(self):
        v1 = self.manuf.get_all("00:1B:C5")
        v2 = self.manuf.get_all("00:1B:C5:0D")
        v3 = self.manuf.get_all("00:1B:C5:0D:00")
        v4 = self.manuf.get_all("00:1B:C5:0D:00:00")
        v5 = self.manuf.get_all("00:1B:C5:0E:00:00")
        v6 = self.manuf.get_all("00:1B:C5:FF:00:00")
        v7 = self.manuf.get_all("00:1B:C5:01:00:00")
        self.assertEqual(v1.manuf, "IeeeRegi")
        self.assertEqual(v1.manuf_long, "IEEE Registration Authority")
        self.assertEqual(v1, v2)
        self.assertEqual(v1, v3)
        self.assertEqual(v1, v4)
        self.assertEqual(v1, v5)
        self.assertEqual(v1, v6)
        self.assertNotEqual(v1, v7)

    def test_getAllWithSimpleNetmask_returnCorrectMatch(self):
        v1 = self.manuf.get_all("00:1B:C5:00:00:00")
        v2 = self.manuf.get_all("00:1B:C5:00:01:00")
        v3 = self.manuf.get_all("00:1B:C5:00:0F:FF")
        v4 = self.manuf.get_all("00:1B:C5:00:10:00")
        self.assertEqual(v1.manuf, "Convergi")
        self.assertEqual(v1.manuf_long, "Converging Systems Inc.")
        self.assertEqual(v1, v2)
        self.assertEqual(v2, v3)
        self.assertNotEqual(v3, v4)

    def test_getAllWithComplexNetmask_returnCorrectMatch(self):
        v1 = self.manuf.get_all("01:80:C2:00:00:2F")
        self.assertEqual(v1.manuf, None)
        self.assertEqual(v1.comment, None)
        v2 = self.manuf.get_all("01:80:C2:00:00:30")
        v3 = self.manuf.get_all("01:80:C2:00:00:37")
        self.assertEqual(v2.manuf, "OAM-Multicast-DA-Class-1")
        self.assertEqual(v2.comment, None)
        self.assertEqual(v2, v3)
        v4 = self.manuf.get_all("01:80:C2:00:00:38")
        v5 = self.manuf.get_all("01:80:C2:00:00:3F")
        self.assertEqual(v4.manuf, "OAM-Multicast-DA-Class-2")
        self.assertEqual(v4.comment, None)
        self.assertEqual(v4, v5)
        v6 = self.manuf.get_all("01:80:C2:00:00:40")
        self.assertEqual(v6.manuf, "All-RBridges")
        self.assertEqual(v6.comment, None)
        v7 = self.manuf.get_all("01:80:C2:00:00:1E")
        self.assertEqual(v7.manuf, "Token-Ring-all-DTR-Concentrators")
        self.assertEqual(v7.comment, None)


