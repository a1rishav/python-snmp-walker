# python-snmp-walker

## Setup (Ubuntu 18.04)
Install snmp daemon and agent
```buildoutcfg
sudo apt install snmp
sudo apt-get install snmpd
sudo apt-get install libsnmp-dev snmp-mibs-downloader
sudo apt-get install gcc python-dev

snmpwalk -v 2c -c public localhost .
```

## Usage
please check main method in snmp_viewer.py

## References
- **Setup** - https://kb.paessler.com/en/topic/5353-monitoring-linux-problem-snmp-port-not-reachable
- Python Libraries for SNMP get, set, walk etc... :
    - https://easysnmp.readthedocs.io/en/latest/
    - https://pypi.org/project/pysnmp/#description
    