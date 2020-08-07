## Getting to the data on a specific .single() item

```python
import tcex


if __name__ == "__main__":
    tc_api_conf = "../tc_config.json"
    tc = tcex.TcEx(config_file=tc_api_conf)
    
    TC_OWNER = "Org owner"
    group_type = "Intrusion Set"
    group_id = 314159
    
    parameters = {'includes': ['additional', 'attributes', 'labels', 'tags']}
    group = tc.ti.group(group_type=group_type, owner=TC_OWNER, unique_id=group_id)
    response = group.single(params=parameters)
    group_resp = response.json().get("data", {})
    
    # get first field by key index - first field key is the type name so it's hard to handle case by case
    # https://stackoverflow.com/questions/4326658/how-to-index-into-a-dictionary
    typekey = list(group_resp)[0]
    group_data = group_resp[typekey]
    print(group_data)
    
    i = group.indicator_associations(params=parameters)
    for indicator in i:
        print(indicator)

```
