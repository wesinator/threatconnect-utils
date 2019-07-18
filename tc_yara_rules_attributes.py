#!/usr/bin/env python3
# parse yara rules from group attributes
import configparser as ConfigParser
import re
import sys
from threatconnect import ThreatConnect

# https://docs.threatconnect.com/en/latest/python/quick_start.html#standard-script-heading
config = ConfigParser.RawConfigParser()
config.read('./tc.conf')

try:
    api_access_id = config.get('threatconnect', 'api_access_id')
    api_secret_key = config.get('threatconnect', 'api_secret_key')
    api_default_org = config.get('threatconnect', 'api_default_org')
    api_base_url = config.get('threatconnect', 'api_base_url')
    
    api_result_limit = config.get('threatconnect', 'api_result_limit')
except ConfigParser.NoOptionError:
    print('Could not read configuration file.')
    sys.exit(1)

tc = ThreatConnect(api_access_id, api_secret_key, api_default_org, api_base_url)
tc.set_api_result_limit(1000)

# instantiate Owners object
#owners = tc.owners()
owners = ['ThreatConnect Intelligence', 'Common Community']

groups = tc.groups()

filter1 = groups.add_filter()
# only retrieve Groups from the given owner(s)
filter1.add_owner(owners)

try:
    groups.retrieve()
except RuntimeError as e:
    print('Error: {0}'.format(e))
    sys.exit(1)


YARA_RULE_RE = "rule\s+[a-zA-Z_](\w{0,127})\s*?{"
for group in groups:
    #print(group.name)
    
    # load the attributes
    group.load_attributes()
    for attribute in group.attributes:
        content = attribute.value
        
        # check if yara rule decl in attribute
        if re.search(YARA_RULE_RE, content):
            print(group.name, group.weblink)
            print(attribute.type)
            
            # Indent yara vars
            content = content.replace("\n$", "\n    $")
            print(content)
