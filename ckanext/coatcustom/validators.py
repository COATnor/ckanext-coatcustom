import ckanext.coatcustom.helpers as helpers
import ckan.plugins.toolkit as toolkit
from ckan.common import config
from ckan.lib.navl import validators as ckan_validators

def required_custom(key, data, errors, context):
    extras = data.get(('__extras',), {})
    if extras.get('__parent'):
        ckan_validators.ignore_missing(key, data, errors, context)
    else:
        ckan_validators.not_empty(key, data, errors, context)

def str_to_bool(value):
    return str(value).lower() == "true"

def bool_to_str(value):
    return str(value)

def multiple_to_string(iterable):
    if not iterable:  # Missing object
        iterable = ""
    if type(iterable) != list:
        return iterable
    return ",".join(iterable)

def select_parent_locations(selected_values):
    if not selected_values:
        return []
    if type(selected_values) != list:
        selected_values = selected_values.split(',')
    generated = set(selected_values)
    choices = helpers.scheming_locations_choices(None)
    value_to_label = {c['value']:c['label'] for c in choices}
    label_to_value = {c['label']:c['value'] for c in choices}
    sep = " - "
    for selected_value in selected_values:
        selected_label = value_to_label[selected_value]
        for parts in range(selected_label.count(sep)):
            section = selected_label.rsplit(sep, parts+1)[0]
            if section in label_to_value:
                generated.add(label_to_value[section])
            else:
                pass  # this should not happen
    return list(generated)

def citation_autocomplete(key, data, errors, context):
    data[key] = ''
    pkg = context.get('package')
    if not pkg:
        return
    pkg_dict = toolkit.get_action('package_show')(
        context, {'id': pkg.id})
    url = config['ckan.site_url'] + "/dataset/" + pkg.name
    if pkg.author:
        data[key] += pkg.author + " et al., "
    data[key] += str(pkg.metadata_modified.year) + ", " + \
                 pkg.name + ": COAT project data. " + \
                 "Available online: " + url
