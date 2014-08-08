manuf.py
===

Parser utility for Wireshark's OUI database.
---

Optimized for quick lookup performance by reading the entire file into memory
on initialization. Maps ranges of MAC addresses to manufacturers and comments
(descriptions). Contains full support for netmasks and other strange things in
the database.

See [Wireshark's OUI lookup tool](https://www.wireshark.org/tools/oui-lookup.html).

Written by Michael Huang.

Copying
---
This library does not link to Wireshark's manuf database, so I have chose to
publish it under the LGPLv3 instead of the GPLv2. The manuf database is provided
for your convenience.

* License for python library: LGPLv3
* License for manuf database: GPLv2

The latest version of the manuf database can be found in the
[Wireshark git repository](https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf).
The database there is updated about once a week.
