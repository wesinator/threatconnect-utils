def get_group_indicators(group_type, group_id, owner):
    """Get group data and indicators associated with a specific group"""
    tc = tc_init()
    parameters = {'includes': ['additional', 'attributes', 'labels', 'tags'],
                  "includeAdditional": "true",
                 }
    ti = tc.ti
    tc_group = ti.group(group_type=group_type, owner=owner, unique_id=group_id)
    #response = ti.single(params=parameters)
    #print(response)
    group = tc_group.single(params=parameters)
    print(group.json())

    group_indicators = []

    # get indicator associations
    c = 0
    all_indicator_params = {
        "includeAdditional": "true", 
        "filters": "active=true,active=false", 
        "orParams": "true"
    }
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
