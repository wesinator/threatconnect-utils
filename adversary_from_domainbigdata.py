from domainbigdata import DomainBigData
from tcex import TcEx

tcex = TcEx()
#tcex.inputs.config_file('app_config.json') # tcex >= 1.1.3
tcex.tcex_args.config_file('app_config.json')
args = tcex.args

org = "Org owner"

group_type = "Adversary"

email = input("Enter email to get domains from DomainBigData: ").strip()

parameters = {'includes': ['additional', 'attributes', 'labels', 'tags']}
ti = tcex.ti

d = DomainBigData()
d.email_lookup(email)
data = d.intelligence
#print(data)
#print(d.intelligence_list)

registrant_name = data.get('registrant_name', '')
registrant_org = data.get('registrant_org', '')

email_adversary_name = "%s , %s - %s" % (registrant_name, registrant_org, email)
source = "https://domainbigdata.com/email/" + email

if len(data['associated_domains']) > 0:
    adversary = tcex.ti.group(group_type=group_type, name=email_adversary_name, owner=org)
    response = adversary.create()
    adversary.add_attribute(attribute_type='Source', attribute_value=source, displayed=True)

    group = response.json()
    group_id = group['data']['adversary']['id']
    print(group['data']['adversary']['webLink'])

    for d in data['associated_domains']:
        domain = d.get('domain', '')
        created_date = d.get('creation_date', '')
        registrar = d.get('registrar', '')

        # create domain indicator in TC, associated to incident
        ti = tcex.ti.indicator(indicator_type='Host', owner=org, hostname=domain, dns_active=True, whois_active=True)
        response = ti.create()

        # add associations
        #group_assoc = tcex.ti.group(group_type='Adversary', owner=org, unique_id=group_id)
        response = ti.add_association(target=adversary)

        # add attributes
        description = "Suspicious domain registered by _%s_" % email
        response = ti.add_attribute(attribute_type='Description', attribute_value=description, displayed=True)

        response = ti.add_attribute(attribute_type='Source', attribute_value=source, displayed=True)

        domain_reg_attribute = "Registrar: %s\nCreated Date: %s\n" % (registrar, created_date)
        response = ti.add_attribute(attribute_type='Additional Analysis and Context', attribute_value=domain_reg_attribute)

        print(domain)
        #print(d)
