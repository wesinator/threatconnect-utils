## Getting associated groups from indicator(s)

```python
import tcex


if __name__ == "__main__":
    tc_api_conf = "tc_config.json"
    tc = tcex.TcEx(config_file=tc_api_conf)
    
    TC_OWNER = "Org owner"
    TC_INDICATOR_TYPE = "Address"
    
    parameters = {'includes': ['additional', 'attributes', 'labels', 'tags']}
    indicators = tc.ti.indicator(indicator_type=TC_INDICATOR_TYPE, owner=TC_OWNER)
    
    for indicator in indicators.many(params=parameters):
        # "summary" field for .many() without indicator type, else the field key is the specific type
        indicator_id = indicator.get("summary", indicator.get("ip", ""))
        
        # check groups for report group
        # https://docs.threatconnect.com/en/latest/tcex/module_threat_intelligence.html#get-indicator-metadata
        indicator_obj = tc.ti.indicator(indicator_type=TC_INDICATOR_TYPE, owner=TC_OWNER, unique_id=indicator_id)
        for group in indicator_obj.group_associations():
            name = group.get("name", "")
            print(name)
```
