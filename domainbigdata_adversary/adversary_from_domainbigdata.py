#!/usr/bin/env python3
import domainbigdata
import tcex
import webbrowser


def tc_init():
    tc_api_conf = "tc_config.json"

    # load config init depending on TcEx version
    if tcex.__version__ < "1.1.0":
        # Init TC connector objects
        tc = tcex.TcEx()
        tc.tcex_args.config_file(tc_api_conf)

        # this is required to init args properly, apparently
        # the returned object doesn't have proper args if leaving this out
        tc.args

    else:
        tc = tcex.TcEx(config_file=tc_api_conf)
        tc.args

    return tc

tcex = tc_init()


# Check if group containing text already exists in TC
def tcGroupExists(type, owner, query):
    existing = {}

    groups = tcex.ti.group(group_type='Adversary', owner=owner)
    for group in groups.many():
        if query.lower() in group["name"].lower():
            existing = group

    return existing


def domainbigdataToTC(email):
    org = tcex.args.api_default_org
    group_type = "Adversary"

    #parameters = {'includes': ['additional', 'attributes', 'labels', 'tags']}
    ti = tcex.ti

    data = domainbigdata.email_lookup(email)
    registrant = data.registrant

    registrant_name = registrant.get('registrant_name', '')
    registrant_org = registrant.get('registrant_org', '')

    if registrant_org == '':
        email_adversary_name = "%s - %s" % (registrant_name, email)
    else:
        email_adversary_name = "%s , %s - %s" % (registrant_name, registrant_org, email)

    source = "https://domainbigdata.com/email/" + email

    if len(data.domains) > 0:
        # check if group already in TC
        # still useful to get urls first for adding new ones
        exists = tcGroupExists(group_type, org, email)

        if exists:
            link = exists["webLink"]
            print("A group containing that name already exists in ThreatConnect\n%s" % link)
            webbrowser.open(link)
        else:
            adversary = tcex.ti.group(group_type=group_type, name=email_adversary_name, owner=org)
            response = adversary.create()
            adversary.add_attribute(attribute_type='Source', attribute_value=source, displayed=True)

            group = response.json()
            group_id = group['data']['adversary']['id']

            for d in data.domains:
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

            print('%d domains found.' % len(data.domains))
            link = group['data']['adversary']['webLink']
            print(link)
            webbrowser.open(link)


if __name__ == "__main__":
    email = input("Enter email to get domains from DomainBigData: ").strip()
    domainbigdataToTC(email)
