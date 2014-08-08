manuf.py
===

Parser utility for Wireshark's OUI database.
---

Optimized for quick lookup performance by reading the entire file into
memory on initialization. Maps ranges of MAC addresses to manufacturers
and comments (descriptions). Contains full support for netmasks and other
strange things in the database.

See [Wireshark's OUI lookup tool](https://www.wireshark.org/tools/oui-lookup.html).

Written by Michael Huang.

Copying
---
* License for python library: LGPLv3
* License for manuf database: GPLv2
