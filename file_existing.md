#### Check if hash already exists as file in TC

```python
def tc_file_exists(tcex_obj, hash, tc_owner):
    """
    Check if file alreay exists given hash. works with SHA256
    https://threatconnect-inc.github.io/tcex/module_threat_intelligence.html#get-indicator-by-value 
    """
    parameters = {'includes': ['additional', 'attributes', 'labels', 'tags']}
    ti = tcex_obj.ti.indicator(indicator_type='File', owner=tc_owner, unique_id=hash)
    response = ti.single(params=parameters)
    indicator = response.json().get("data", {})
    #print(indicator)
    return indicator

```
