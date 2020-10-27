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

def _associated_datasets(data):
    context = {'ignore_auth': True}
    for name in data.get(('datasets',), '').split(','):
        yield toolkit.get_action('ckan_package_show')(context, {'id': name})

def datasets_visibility(key, data, errors, context):
    if not str_to_bool(data[key]):
        for package in _associated_datasets(data):
            if package['private']:
                raise toolkit.Invalid('Cannot set a state variable as public '
                    'if one or more associated datasets are private')

def merge_from_datasets(key, data, errors, context, sep=",", strip=False):
    values = set()
    for package in _associated_datasets(data):
        value = package.get(key[0])
        if not value:
            continue
        for part in value.split(","):
            if strip:
                part = part.strip()
            values.add(part)
    data[key] = sep.join(values)

def merge_from_datasets_human_readable(key, data, errors, context):
    merge_from_datasets(key, data, errors, context, sep=", ", strip=True)

def merge_tags_from_datasets(key, data, errors, context):
    # Extract tags from datasets
    tags = {}
    for package in _associated_datasets(data):
        for tag in package['tags']:
            tags[tag['name']] = tag
    data[key] = ",".join(tags)
    # Remove old tags
    for data_key in data.keys():
        if data_key[0] == 'tags':
            del data[data_key]
    # Create new tags
    toolkit.get_validator('tag_string_convert')(key, data, errors, context)
