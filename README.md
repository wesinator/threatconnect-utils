# threatconnect-utils
Script utilities, programming snippets, and configs for using the ThreatConnect API and analysis.

## Impetus

Solving intel, implementation, and data quality problems commonly encountered in ThreatConnect data.
TC documentation (as with many vendor documentation) does not provide many higher-level examples of how to use the API to solve actual TI, data quality problems.


### Inconsistencies in TcEx API interface

Some inconsistencies in the [TcEx](https://github.com/ThreatConnect-Inc/tcex) python API interface that I aim to address or at least document in this project:

#### [TI module](https://threatconnect-inc.github.io/tcex/module_ti.html):
  ##### Item data access
  - items `.many()` returns accesible data object
  
  - `.single()` for getting a specific indicator or group returns a response object that has to be accessed by one of the following:
    - `response.text` (an attribute/property)
    - `response.json()` (a function)
      - this should also be a property to be consistent. The json function can be done behind the property

  ##### Indicator access
  - Specific indicators can be accessed either by `ti.indicator(` with a [unique_id](https://threatconnect-inc.github.io/tcex/module_ti.html?highlight=json#get-indicator-by-value)
  
    or 
    
    `ti.<indicator_type>` with an `<indicator_type>=` keyword arg
    
    the keyword arg should be consistent

