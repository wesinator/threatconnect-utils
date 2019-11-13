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
    args = tc.args

```

#### init function:
```python3
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

```
