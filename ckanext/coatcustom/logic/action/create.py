import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
from ckanext.coat.logic.action.create import package_create as coat_package_create
from ckanext.scheming.helpers import scheming_get_dataset_schema
import json

_get_or_bust = logic.get_or_bust

#@toolkit.side_effect_free
@toolkit.chained_action
def package_create(coat_package_create, context, data_dict):
    if data_dict.get('__parent', False):
        return coat_package_create(context, data_dict)

    # parent dataset
    # https://github.com/aptivate/ckanext-datasetversions/issues/10

    t = _get_or_bust(data_dict, 'type')
    expanded = data_dict.get('expanded', True)
    s = scheming_get_dataset_schema(t, expanded)
    #data_dict['temp'] = s

    e = 0.001  # epsilon
    geometry = {
        'type': 'MultiPolygon',
        'coordinates': [],
    }

    for field in s['dataset_fields']:
        if field['field_name'] != 'location':
            continue
        for choice in field['choices']:
            if choice['value'] not in data_dict['location']:
                continue
            lon = choice['lon']
            lat = choice['lat']
            geometry['coordinates'].append([[
                [lon-e, lat-e],
                [lon-e, lat+e],
                [lon+e, lat+e],
                [lon+e, lat-e],
                [lon-e, lat-e],
            ]])

    data_dict.setdefault('extras', [])  #?

    value = json.dumps(geometry)
    data_dict['extras'].append({'key': 'spatial', 'value': value})
    data_dict['spatial'] = value  # serve?

    return coat_package_create(context, data_dict)