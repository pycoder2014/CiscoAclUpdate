# CiscoAclUpdate

## Overview

Script to update ACL on Cisco IOS devices.

The script read the input from the params yaml file, connects to each of the listed devices then update the device ACL. Pre and post-change configs for each device are saved to the config folder.



## Installation


```console

git clone https://github.com/pycoder2014/CiscoAclUpdate.git
cd CiscoAclUpdate
pip install -r requirements.txt

```

## Usage

Add parameters to the (params.yaml) yaml file.


```yaml
hosts:
  - 192.168.101.10

access-list:
  access-list 10:
    - access-list 10 permit 192.168.101.0 0.0.0.255
    - access-list 10 permit 192.168.102.0 0.0.0.255
    - access-list 10 permit 192.168.103.0 0.0.0.255

``` 

Execute script.


```console
> python .\script.py

Username : user1
Password :
Connecting to 192.168.101.10 : OK
        before config saved to configs\192.168.101.10_before.txt
        Updating access-list 10
        update successful.
        after config saved to configs\192.168.101.10_after.txt
        save config.
```

