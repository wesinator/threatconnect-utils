#### Initialise TcEx properly 

```python3
#!/usr/bin/env python3
import tcex

tc_api_conf = 'tc_config.json'

# load config init depending on TcEx version
if tcex.__version__ < "1.1.0":
    tc = tcex.TcEx()
    tc.tcex_args.config_file(tc_api_conf)
    args = tc.args

else:
    tc = tcex.TcEx(config_file=tc_api_conf)


```
