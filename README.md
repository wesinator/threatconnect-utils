# threatconnect-utils
Script utilities, programming snippets, and configs for using the ThreatConnect API and analysis.

## Impetus

Solving intel, implementation, and data quality problems commonly encountered in ThreatConnect data.
TC documentation (as with many vendor documentation) does not necessarily provide many higher-level examples of how to use the API to solve actual TI, data quality problems.

## TcEx

### Inconsistencies in TcEx API interface

Some inconsistencies in the [TcEx](https://github.com/ThreatConnect-Inc/tcex) python API interface that I aim to address or at least document in this project:

#### [TI module](https://threatconnect-inc.github.io/tcex/module_ti.html):
  ##### Item data access
  - items `.many()` returns a more generic, accessible data object
  
  - `.single()` for getting a specific indicator or group returns a response object that has to be accessed by one of the following python `requests` object properties:
    - `response.text`
    - `response.json()`

  ##### Indicator access
  - Specific indicators can be accessed either by `ti.indicator(` with a [unique_id](https://threatconnect-inc.github.io/tcex/module_ti.html?highlight=json#get-indicator-by-value)
  
    or 
    
    `ti.<indicator_type>` with an `<indicator_type>=` keyword arg
    
    the keyword arg should be consistent

### Error handling
Handle potential network exception on retrieving items with `.many()`:
```python
    try:
        for group in groups.many(params=parameters):
            #print(group)
            # Do stuff here
    except Exception as e:
        print("Error retrieving from TC API: ", repr(e))
```

#

```python
# handle connection timeout, conn errors from requests module
    try:
        response = ti.create()
    except requests.exceptions.ConnectionError as e:
        print("Error creating object in TC:", e)
```
