### Get all associated indicators regardless of status:

https://github.com/ThreatConnect-Inc/threatconnect-developer-docs/blob/1ae8a1c76078177a551860ada3aac88af124b47f/docs/rest_api/indicators/filters.rst

`GET /v2/indicators?filters=active%3Dtrue,active%3Dfalse&orParams=true`

#### parameter struct:
```json
{
    "includeAdditional": "true", 
    "filters": "active=true,active=false", 
    "orParams": "true"
}
```

#### TC-JS
```javascript
/*
 * filter on active + inactive indicators
 * https://docs.threatconnect.com/en/latest/javascript/javascript_sdk.html#filters
*/
indicatorStatusFilter = new Filter(FILTER.OR);
indicatorStatusFilter.on('active', FILTER.EQ, 'true');
indicatorStatusFilter.on('active', FILTER.EQ, 'false');

```

#### TcEx (v1.0.6):
```python
#!/usr/bin/env python3
from tcex import TcEx

tcex = TcEx()
tcex.tcex_args.config_file('app_config.json')
args = tcex.args

owner = "Owner org"
group_type = "Incident"

ti = tcex.ti

inc_id = 1234

parameters = {'includes': ['additional', 'attributes', 'labels', 'tags']}

group = ti.group(group_type=group_type, owner=owner, unique_id=inc_id)

# filters for both active or inactive status indicators
all_indicator_params = {"includeAdditional": "true",
                        "filters": "active=true,active=false",
                        "orParams": "true"}

c = 0
for indicator in group.indicator_associations(params=all_indicator_params):
    print(indicator['webLink'])
    c += 1

print("%d indicators" % c)

```
