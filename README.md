manuf
===

[![Build Status](https://github.com/coolbho3k/manuf/workflows/test/badge.svg)](https://github.com/coolbho3k/manuf/actions)
[![Build Status](https://badge.fury.io/py/manuf.svg)](https://pypi.org/project/manuf/)

Parser library for Wireshark's OUI database.
---

Converts MAC addresses into a manufacturer using Wireshark's OUI database.

Optimized for quick lookup performance by reading the entire file into memory
on initialization. Maps ranges of MAC addresses to manufacturers and comments
(descriptions). Contains full support for netmasks and other strange things in
the database.

See [Wireshark's OUI lookup tool](https://www.wireshark.org/tools/oui-lookup.html).

Written by Michael Huang (coolbho3k).

Install
---

#### With PyPi

    pip install manuf

#### Or Manually

    git clone https://github.com/coolbho3k/manuf
    cd manuf
    python setup.py install

Usage
---

#### As a library:

    >>> from manuf import manuf
    >>> p = manuf.MacParser(update=True)
    >>> p.get_all('BC:EE:7B:00:00:00')
    Vendor(manuf='AsustekC', comment='ASUSTek COMPUTER INC.')
    >>> p.get_manuf('BC:EE:7B:00:00:00')
    'AsustekC'
    >>> p.get_comment('BC:EE:7B:00:00:00')
    'ASUSTek COMPUTER INC.'

#### As a command line:

    $ manuf BC:EE:7B:00:00:00
    Vendor(manuf='AsustekC', comment='ASUSTek COMPUTER INC.')
    
Use a manuf file in a custom location:

    $ manuf --manuf ~/manuf BC:EE:7B:00:00:00
    Vendor(manuf='AsustekC', comment='ASUSTek COMPUTER INC.')

Automatically update the manuf file from Wireshark's git:

    $ manuf --update BC:EE:7B:00:00:00
    Vendor(manuf='AsustekC', comment='ASUSTek COMPUTER INC.')

Note, that this command will update the manuf file bundled with this package. If you do not wish to 
modify this, or do not have permissions to do so, you must specify a custom manuf file to perform an update.

    $ manuf --update --manuf ~/manuf BC:EE:7B:00:00:00
    Vendor(manuf='AsustekC', comment='ASUSTek COMPUTER INC.')

Alternatively you can call the program with:

    python -m manuf
or by executing the `manuf.py` script directly

```bash
./manuf/manuf.py # From the install folder
```

Features and advantages of manuf
---

Note: the examples use the manuf file provided in the first commit, 9a180b5.

manuf.py is more accurate than more naive scripts that parse the manuf file.
Critically, it contains support for netmasks.

For a usual entry, such as BC:EE:7B (AsustekC), the manufacturer "owns" the
last half (24 bits) of the MAC address and is free to assign the addresses
BC:EE:7B:00:00:00 through BC:EE:7B:FF:FF:FF, inclusive, to its devices.

However, entries like the following also appear commonly in the file:

    00:1B:C5:00:00:00/36	Convergi               # Converging Systems Inc.
    00:1B:C5:00:10:00/36	OpenrbCo               # OpenRB.com, Direct SIA

/36 is a netmask, which means that the listed manufacturer "owns" only the last
12 bits of the MAC address instead of the usual 24 bits (since MAC addresses
are 48 bits long, and 48 bits - 36 bits = 12 bits).

This means that Converging Systems is only free to assign the addresss block
00:1B:C5:00:00:00 through 00:1B:C5:00:0F:FF. Anything after that belongs to
other manufacturers. manuf.py takes this fact into account:

    >>> p.get_manuf('00:1B:C5:00:00:00')
    'Convergi'
    >>> p.get_manuf('00:1B:C5:00:0F:FF')
    'Convergi'
    >>> p.get_manuf('00:1B:C5:00:10:00')
    'OpenrbCo'

Even Wireshark's web lookup tool fails here. "00:1B:C5:00:0F:FF" returns only
"IEEE REGISTRATION AUTHORITY" while it should instead return "Converging
Systems Inc." If a netmask is not explicitly specified, a netmask of /24 is
implied. Since this covers most of the entries, most tools only parse the first
24 bits.

manuf.py fully supports even more esoteric entries in the database. For example,
consider these two entries:

    01-80-C2-00-00-30/45	OAM-Multicast-DA-Class-1
    01-80-C2-00-00-38/45	OAM-Multicast-DA-Class-2

With a netmask of /45, only the last 3 bits of the address are significant.
This means that a device is considered "OAM-Multicast-DA-Class-1" only if the
last digit falls between 0x0 and 0x7 and "OAM-Multicast-DA-Class-2" only if the
last digit falls between 0x8 and 0xF.

If the last octet is 0x40 or over, or 0x2F or under, the address doesn't belong
to any manufacturer.

    >>> p.get_manuf('01:80:C2:00:00:2F')
    >>> p.get_manuf('01:80:C2:00:00:30')
    'OAM-Multicast-DA-Class-1'
    >>> p.get_manuf('01:80:C2:00:00:37')
    'OAM-Multicast-DA-Class-1'
    >>> p.get_manuf('01:80:C2:00:00:38')
    'OAM-Multicast-DA-Class-2'
    >>> p.get_manuf('01:80:C2:00:00:3F')
    'OAM-Multicast-DA-Class-2'
    >>> p.get_manuf('01:80:C2:00:00:40')

Again, the official lookup tool fails here as well, with "01:80:C2:00:00:31"
returning no results.

Algorithm
---

Although optimized for correctness, manuf.py is also quite fast, with average
O(1) lookup time, O(n) setup time, and O(n) memory footprint.

First, the entire manuf file is read into memory. Each manuf line is stored in
a dict mapping a tuple calculated from the MAC address and netmask to each
manuf:

    ((48 - netmask), macaddress >> (48 - netmask))

The (48 - netmask) value is called the "bits left" value in the code.

For example, Converging Systems' MAC is 0x001BC5000000 and its netmask is 36,
so its key in the dict is this:

    (12, 0x001BC5000000 >> 12)

To lookup "00:1B:C5:00:0F:FF" we will check the dict beginning with a "bits
left" value of 0, incrementing until we find a match or go over 47 (which means
we have no match):

    (0, 0x001BC5000FFF >> 0)
    (1, 0x001BC5000FFF >> 1)
    (2, 0x001BC5000FFF >> 2)
    ...
    (12, 0x001BC5000FFF >> 12)

Since (12, 0x001BC5000FFF >> 12) equals (12, 0x001BC5000000 >> 12), we have a
match on the 13th iteration of the loop.

Copying
---

This library does not link to Wireshark's manuf database; it merely parses it,
so I have chosen to publish it under the LGPLv3 and Apache License 2.0
instead of the GPLv2. The manuf database is provided for your convenience in
this repository, but will not be updated.

* License for Python library: LGPLv3 and Apache License 2.0 (dual licensed)
* License for manuf database: GPLv2

The latest version of the manuf database can be found in the
[Wireshark git repository](https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf).
The database there is updated about once a week, so you may want to grab the
latest version to use instead of using the one provided here by using the
--update flag on the command line:

    manuf --update

Run tests
---

    python -m unittest manuf.test.test_manuf
