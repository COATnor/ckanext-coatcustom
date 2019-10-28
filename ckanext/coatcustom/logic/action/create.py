import ckan.plugins.toolkit as toolkit
from ckanext.coat.logic.action.create import package_create as coat_package_create
import json

#@toolkit.side_effect_free
@toolkit.chained_action
def package_create(coat_package_create, context, data_dict):
    # parent dataset
    # https://github.com/aptivate/ckanext-datasetversions/issues/10
    if data_dict.get('__parent', False):
        return coat_package_create(context, data_dict)

    data_dict.setdefault('extras', [])

    json_string = '''
                {
                    "type": "Point",
                     "coordinates": [-3.145,53.078]
                }
                '''
    value =  json_string
    for extra in data_dict['extras']:
        if extra['key'] == 'spatial':
            extra['value'] = value
            break
    else:
        data_dict['extras'].append({'key': 'spatial', 'value': value})
    data_dict['spatial'] = value

    return coat_package_create(context, data_dict)