#!/usr/bin/env python3
# renames tags matching a given pattern with an appended string
# https://threatconnect-inc.github.io/tcex/examples.html?highlight=tcex%20resources%20tag%20tcex#retrieve-all-tags
import json

from tcex import TcEx

tcex = TcEx()
tcex.tcex_args.config_file('app_config.json')
args = tcex.args

# tag with 'World' will become 'Hello World'
tag_match = "World"
tag_update = "Hello "

owner = "Org owner"


def main():
    resource = tcex.resources.Tag(tcex)
    resource.owner = owner
    resource.url = args.tc_api_path

    for results in resource:  # pagination
        if results.get('status') == 'Success':
            #print(json.dumps(results.get('data', []), indent=4))
            
            for tag in results['data']:
                name = tag['name']
                
                if tag_match in name and tag_update not in name:
                    print(name)
                    
                    new_tag = tag_update + name
                    new_tag_data = {"name": new_tag}
                    
                    resource.http_method = 'PUT'
                    resource.body = json.dumps(new_tag_data)
                    print(resource.body)
                    
                    resource._request_uri = 'tags/' + name
                    response = resource.request()
                    print(response)
        else:
            warn = 'Failed retrieving result during pagination.'
            tcex.log.error(warn)


if __name__ == "__main__":
    main()
