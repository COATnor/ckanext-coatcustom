import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
#from ckanext.coat.logic.action.create import package_create as coat_package_create
from ckanext.scheming.helpers import scheming_get_dataset_schema
import ckanext.coatcustom.helpers as helpers
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

    longitudes = []
    latitudes = []
    for field in s['dataset_fields']:
        if field['field_name'] != 'location':
            continue
        for choice in helpers.scheming_locations_choices(None):
            if choice['value'] not in data_dict.get('location', []):
                continue
            longitudes.append(choice['lon'])
            latitudes.append(choice['lat'])

    if not longitudes or not latitudes:
        return coat_package_create(context, data_dict)

    lon_min, lon_max = min(longitudes), max(longitudes)
    lat_min, lat_max = min(latitudes), max(latitudes)
    geometry = {
        'type': 'Polygon',
        'coordinates': [[
            [lon_min, lat_max],
            [lon_max, lat_max],
            [lon_max, lat_min],
            [lon_min, lat_min],
            [lon_min, lat_max],
        ]],
    }

    data_dict.setdefault('extras', [])  #?

    value = json.dumps(geometry)
    data_dict['extras'].append({'key': 'spatial', 'value': value})
    data_dict['spatial'] = value  # serve?

    return coat_package_create(context, data_dict)