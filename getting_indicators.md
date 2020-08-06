# Getting indicators the sane way

TCEx and the TC API unfortunately gives three different object structures for indicator data (even though it's the same data for each indicator), depending on how you request the indicator.

The flattest, most 'sane' object is given in tcex by calling `indicators.many()` _without_ a type filter.

This object structure has the following primary fields:
 - `type`: the TC indicator type
 - `summary`: the indicator 'value'

#### Getting a single indicator flat object structure
```python
import tcex


if __name__ == "__main__":
    tc_api_conf = "../tc_config.json"
    tc = tcex.TcEx(config_file=tc_api_conf)
    
    TC_OWNER = "Org owner"
    parameters = {'includes': ['additional', 'attributes', 'labels', 'tags']}
    
    lookup_indicator = "example.com"
    
    # https://docs.threatconnect.com/en/latest/tcex/module_threat_intelligence.html#get-indicators-by-filter
    filters = tc.ti.filters()
    filters.add_filter('summary', '=', lookup_indicator)
    
    indicators = tc.ti.indicator(owner=TC_OWNER)
    for indicator in indicators.many(filters=filters, params=parameters):
        print(indicator)

```
