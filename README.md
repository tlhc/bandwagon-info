#bwi.py

bwi.py is a simple script for get bandwagonhost.com vps status info


![screen:](https://raw.githubusercontent.com/tlhc/bandwagon-info/master/bwg.png)

![screen-all:](https://raw.githubusercontent.com/tlhc/bandwagon-info/master/bwg-all.png)


config file:

``` cfg
[info]
local_use = 0             ;local_use: '1' for run on vps and the vps_ip parm can be empty
                          ;local_use: '0' for run on other pc and need vps_ip config
vps_ip = xxx.xxx.xxx.xxx  ;vps ip address
manage_host = host_url    ;your kiwivm manage host url
manage_pass = pass        ;your kiwivm manage password
```

example:
``` cfg
[info]
local_use = 0                                ;on my pc
vps_ip = 111.111.111.111                     ;my vps node ip address
manage_host = https://kiwivm.64clouds.com/   :your kiwivm manage password
manage_pass = mypassword                     ;your kiwivm manage password
```

usage:

``` bash
python bwi.py                                   #default for all info

python bwi.py -c ./bwi.cfg -s 'node ram swap disk reset bandwidth time'
              
               -c path to your config file
               -s show info switch (you can just config 'ram bandwidth' for ram and bandwidth info)
```
or add below to your .bashrc or (.zshrc)

``` bash
alias bwi='cd /path/to/bandwagon-info; python bwi.py; cd -;'
```

todo:
- control vps start stop reboot and etc
