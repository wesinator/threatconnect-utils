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


def tcFileFromVT(tcex_client, vt_data, tc_owner="", tc_hash=""):
    """Takes VT api file data, creates file in TC, or updates existing TC file"""
    file = {
        "md5": vt_data.md5,
        "sha1": vt_data.sha1,
        "sha256": vt_data.sha256,
        "sha512": vt_data.__dict__.get("sha512", ""), # SHA512 might not be present on VT file
        "size": vt_data.size,
    }

    if not tc_owner:
        tc_owner = tcex_client.args.api_default_org

    tc_file = tcex_client.ti.indicator(
        indicator_type='File',
        owner=tc_owner,
        md5=file["md5"],
        sha1=file["sha1"],
        sha256=file["sha256"],
        size=file["size"]
    )

    try:
        if not tc_hash:
            response = tc_file.create()
        else:
            response = tc_file.update()
        print(response.json())

        if file["sha512"]:
            tc_file.add_attribute(attribute_type='SHA512 Hash', attribute_value=file["sha512"])
    except Exception as e:
        print(e)
