# check_air_purifier

check_air_purifier.py is a python 3 script for monitoring air purifiers made by philips. Communication with the device is made with a customized version of py-air-control. Tested with AC1214_10, but should work with any other philips device.

Features:

* Monitor air-quality (allergen index / pm2.5) and filter status including thresholds and perfdata
* Check device status (fan speed, power, light, updates, network)


## Installation

Use the package manager [pip3](https://pip.pypa.io/en/stable/) to install the required module py-air-control (tested with version 0.5.0).

```bash
pip3 install py-air-control
```

Put the plugin into libexec and extend your checkcommands. For icinga2 you can use check_air_purifier.cfg.

## Usage

```
usage: check_air_purifier.py [-h] -H HOSTNAME -m
                             {deviceinfo,filters,airquality} [-w WARNING]
                             [-c CRITICAL]

optional arguments:
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname HOSTNAME
                        Hostname / IP of air purifier
  -m {deviceinfo,filters,airquality}, --mode {deviceinfo,filters,airquality}
                        mode to check
  -w WARNING, --warning WARNING
                        Warning threshold
  -c CRITICAL, --critical CRITICAL
                        Critical threshold
```

## Examples

```bash
check_air_purifier.py -H 192.168.10.120 -m 'deviceinfo'
OK: Power is ON - Mode is auto - Fan Speed is 2 - Light brightness is 50 - Button Light is ON - Used Index is IAI - Child lock is False - name is AC1214_10 - version is 2 - upgrade is  - state is idle - progress is 0 - statusmsg is  - mandatory is False - ssid is myssid - password is mypassword - protection is wpa-2 - ipaddress is 192.168.10.120 - netmask is 255.255.255.0 - gateway is 192.168.10.1 - dhcp is True - macaddress is mymacaddress - cppid is mycppid|'Fan Speed'=2 'Light brightness'=50 

check_air_purifier.py -H 192.168.10.120 -m 'filters' --warning 16 --critical 8
OK: Pre-filter and Wick is ok (44 hours remaining) - Active carbon filter is ok (2084 hours remaining) - HEPA filter is ok (4484 hours remaining)|'Pre-filter and Wick'=44 'Active carbon filter'=2084 'HEPA filter'=4484

check_air_purifier.py -H 192.168.10.120 -m 'airquality' --warning 8 --critical 10
OK: Allergen index is ok (4) - PM25 is 19|'Allergen index'=4 'PM25'=19
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
