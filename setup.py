from setuptools import setup
# The text of the README file
README = open("./README.md",'r').read()
setup(
    name = 'manuf',
    packages = ['manuf'],
    version = '1.1.0',
    description = 'Parser library for Wireshark\'s OUI database',
    author = 'Michael Huang',
    url = 'https://github.com/coolbho3k/manuf/',
    license = 'Apache License 2.0 or GPLv3',
    keywords = ['manuf', 'mac address', 'networking'],
    entry_points = {
        'console_scripts': [
            'manuf=manuf.manuf:main'
        ],
    },
    package_data = {
        'manuf': ['manuf']
    },
    long_description    =   README,
    long_description_content_type   =   "text/markdown"
)

