#!/usr/bin/env python

# manuf.py: Parser utility for Wireshark's OUI database.
# Copyright (c) 2014, Michael Huang
#
# This library is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, see
# <http://www.gnu.org/licenses>.

import re
import sys

from collections     import defaultdict
try:
    from cStringIO   import StringIO
except ImportError:
    from StringIO    import StringIO

class MacParser(object):
    """Class that contains a parser for Wireshark's OUI database.

       Optimized for quick lookup performance by reading the entire file into
       memory on initialization. Maps ranges of MAC addresses to manufacturers
       and comments (descriptions). Contains full support for netmasks and other
       strange things in the database.

       See https://www.wireshark.org/tools/oui-lookup.html

       Attributes:
         attr1 (str): Location of the manuf database file.

    """

    def  __init__(self, manuf_name="manuf"):
        self._pattern = re.compile("[-:\.]")
        with open(manuf_name, 'r+') as f:
            self._manuf_file = StringIO(f.read())
        self._masks = {}

        # Build mask -> result dict
        for line in iter(self._manuf_file.readline, ''):
            com = line.split('#', 1)
            arr = com[0].split()

            if len(arr) < 1:
                continue

            parts = arr[0].split('/')
            mac_str = self._strip_mac(parts[0])
            mac_int = self._get_mac_int(mac_str)
            mask = self._bits_left(mac_str)

            # Specification includes mask
            if len(parts) > 1:
                mask_spec = 48 - int(parts[1])
                if mask_spec > mask:
                    mask = mask_spec

            if len(com) > 1:
                result = (arr[1], com[1].strip())
            else:
                result = (arr[1], None)

            self._masks[(mask,  mac_int >> mask)] = result

        self._manuf_file.close()

    def get_all(self, mac):
        """Get a tuple containing (manufacturer, comment) from a MAC address.

        Attributes:
          attr1 (str): MAC address in standard format.

        Returns:
          Tuple containing (manufacturer, comment). Either or both may be None
          if not found.

        Raises:
          ValueError: If the MAC could not be parsed.

        """
        mac_str = self._strip_mac(mac)
        mac_int = self._get_mac_int(mac_str)

        # If the user only gave us X bits, check X bits. No partial matching!
        for mask in xrange(self._bits_left(mac_str), 48):
            result = self._masks.get((mask, mac_int >> mask))
            if result:
                return result
        return (None, None)

    def get_manuf(self, mac):
        """Returns manufacturer from a MAC address.

        Attributes:
          attr1 (str): MAC address in standard format.

        Returns:
          String containing manufacturer, or None if not found.

        Raises:
          ValueError: If the MAC could not be parsed.

        """
        return self.get_all(mac)[0]

    def get_comment(self, mac):
        """Returns comment from a MAC address.

        Attributes:
          attr1 (str): MAC address in standard format.

        Returns:
          String containing comment, or None if not found.

        Raises:
          ValueError: If the MAC could not be parsed.

        """
        return self.get_all(mac)[1]

    # Gets the integer representation of a stripped mac string
    def _get_mac_int(self, mac_str):
        try:
            # Fill in missing bits with zeroes
            return int(mac_str, 16) << self._bits_left(mac_str)
        except ValueError:
            raise ValueError("Could not parse MAC: "+str(mac_str))

    # Strips the MAC address of '-', ':', and '.' characters
    _strip_mac = lambda self, mac: self._pattern.sub("", mac)

    # Gets the number of bits left in a mac string
    _bits_left = lambda self, mac_str: 48 - 4 * len(mac_str)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("manuf.py: Parser utility for Wireshark's OUI database.")
        print("    Usage: manuf.py <MAC address>")
    else:
        parser = MacParser()
        print parser.get_all(sys.argv[1])
