#!/usr/bin/env python3

# Use tcex library for TC API
from tcex import TcEx

import dns.resolver
import sys

dns_servers = ['1.1.1.1', '1.0.0.1'] # CloudFlare public DNS


# adopted from https://github.com/xn-twist/xn-twist/blob/b0316f3af0ffa1121179efc2035cce07cfb8944f/xn_twist/xn_twist.py#L86
def get_domain_dns(domain):
    """Get the DNS record, if any, for the given domain."""
    dns_records = list()

    # set DNS server for lookup
    dns_resolver = dns.resolver.Resolver()

    dns_resolver.nameservers = dns_servers

    try:
        # get the dns resolutions for this domain
        dns_results = dns_resolver.query(domain)
        dns_records = [ip.address for ip in dns_results]
        #print(dns_records)
    except dns.resolver.NXDOMAIN as e:
        # the domain does not exist so dns resolutions remain empty
        dns_records = 'NXDOMAIN'
    except dns.resolver.NoAnswer as e:
        # the resolver is not answering so dns resolutions remain empty
        print("the DNS server(s) %s did not answer" % dns_servers, e)
        dns_records = 'SERVFAIL'
    except dns.resolver.NoNameservers as e:
        # the resolver is not answering so dns resolutions remain empty
        print("the nameservers did not answer", e)
        dns_records = 'SERVFAIL'

    return dns_records


tcex = TcEx()
tcex.tcex_args.config_file('app_config.json')
args = tcex.args

owner = "Owner"

_id = sys.argv[1]
group_type = 'Event'

parameters = {'includes': ['additional', 'attributes', 'labels', 'tags']}
ti = tcex.ti.group(group_type=group_type, owner=owner, unique_id=_id)
#response = ti.single(params=parameters)
#print(response)

# get indicator associations
csv = "Domain,IP address,Third column\r\n"

for indicator in ti.indicator_associations():
    #print(indicator)
    host = indicator['summary']
    #print(host)

    res = get_domain_dns(host)

    csv += "%s,%s, \r\n" % (host, str(res))

print("CSV :\n%s\n" % csv)
