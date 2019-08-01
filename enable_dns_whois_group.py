#!/usr/bin/env python3
# Enable DNS and WHOIS on domains associated with specified group id
import sys
from tcex import TcEx

tcex = TcEx()
tcex.tcex_args.config_file('app_config.json')
args = tcex.args

owner = "Owner"

group_type = "Incident"
group_id = input("Enter id of incident to enable DNS and WHOIS: ")


def enable_DNS_WHOIS_group(group_type, group_id, owner=''):
    parameters = {'includes': ['additional', 'attributes', 'labels', 'tags']}
    ti = tcex.ti
    group = ti.group(group_type=group_type, owner=owner, unique_id=group_id)
    #response = ti.single(params=parameters)
    #print(response)

    # get indicator associations
    c = 0
    for indicator in group.indicator_associations():
        if indicator['type'] == "Host":
            ti_host = ti.host(indicator['summary'], owner=owner, 
                            dns_active=True, whois_active=True)
            r = ti_host.update()
            ti_data = r.json()
            print(ti_data)
            
            c += 1

    print("%d hosts enabled DNS and WHOIS" % c)

