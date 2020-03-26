#!/usr/bin/env python3
import tcex


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


def get_group_indicators(group_type, group_id, owner):
    """Get group data and indicators associated with a specific group
    Using .many() in spite of already knowing the group ID, 
    because it returns a flatter base response objecct that is easier to use 
    than .single() response.json() object
    Adds unnecessary API calls to TC but that's a price to pay for better response struct
    """
    tc = tc_init()
    parameters = {'includes': ['additional', 'attributes', 'labels', 'tags'],
                  "includeAdditional": "true",
                 }
    ti = tc.ti
    tc_group = ti.group(group_type=group_type, owner=owner, unique_id=group_id)
    #response = ti.single(params=parameters)
    #print(response)
    for group in tc_group.many(params=parameters):
        #print(group)
    
        if int(group_id) == int(group['id']):
            print(group)
            
            group_name = group['name'].replace(' ', '_').replace(':', '_')
            group_indicators = []
            
            # get indicator associations
            c = 0
            all_indicator_params = {
                "includeAdditional": "true", 
                "filters": "active=true,active=false", 
                "orParams": "true"
            }
            
            # need to re-get specific group object by id to be able to get indicator associations
            tc_group = ti.group(group_type=group_type, owner=owner, unique_id=group_id)
            # indicator_associations is called on initial groups object
            for indicator in tc_group.indicator_associations(params=all_indicator_params):
                print(indicator)
                '''i = ti.indicator(
                    indicator_type=indicator['type'],
                    owner=owner,
                    unique_id=indicator['summary']
                )
                indicator = i.single(params=all_indicator_params)
                print(indicator.json())'''
                c += 1

            print("%d indicators retrieved from %s" % (c, group_name))
