manuf.py
===

Parser utility for Wireshark's OUI database.
---

Converts MAC addresses into a manufacturer using Wireshark's OUI database.

Optimized for quick lookup performance by reading the entire file into memory
on initialization. Maps ranges of MAC addresses to manufacturers and comments
(descriptions). Contains full support for netmasks and other strange things in
the database.

See [Wireshark's OUI lookup tool](https://www.wireshark.org/tools/oui-lookup.html).

Written by Michael Huang (coolbho3k).

Usage
---
    >>> import manuf
    >>> p = manuf.MacParser()
    >>> p.get_all('BC:EE:7B:00:00:00')
    ('AsustekC', 'ASUSTek COMPUTER INC.')
    >>> p.get_manuf('BC:EE:7B:00:00:00')
    'AsustekC'
    >>> p.get_comment('BC:EE:7B:00:00:00')
    'ASUSTek COMPUTER INC.'

Copying
---
This library does not link to Wireshark's manuf database, so I have chosen to
publish it under the LGPLv3 instead of the GPLv2. The manuf database is provided
for your convenience.

* License for Python library: LGPLv3
* License for manuf database: GPLv2

The latest version of the manuf database can be found in the
[Wireshark git repository](https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf).
The database there is updated about once a week, so you may want to grab the
latest version to use.
