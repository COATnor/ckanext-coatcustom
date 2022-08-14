import ckanext.coatcustom.helpers as helpers
import ckan.plugins.toolkit as toolkit
from ckan.common import config
from ckan.lib.navl import validators as ckan_validators
from ckanext.scheming.validation import scheming_load_json

import json

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

def commalist_to_json(value):
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        if type(value) == str:
            return value.split(',')
        else:
            return value

def select_parent_locations(selected_values, sep=" - "):
    if not selected_values:
        return []
    if type(selected_values) == str:
        selected_values = selected_values.split(',')
    elif type(selected_values) == list:
        selected_values = [selected_values]
    generated = set()
    for selected_value in selected_values:
        while sep in selected_value:
            generated.add(selected_value)
            selected_value, _ = selected_value.rsplit(sep, 1)
        generated.add(selected_value)
    return list(generated)

def list_to_tag_string(value):
    if type(value) in (list, set):
        return ','.join(value)
    else:
        return value

def tag_string_to_list(value):
    if type(value) in (list, set):
        return value.split(',')
    else:
        return [value]


def citation_autocomplete(key, data, errors, context):
    data[key] = ''
    pkg = context.get('package')
    if not pkg:
        return
    pkg_dict = toolkit.get_action('package_show')(
        context, {'id': pkg.id})
    url = config['ckan.site_url'] + "/dataset/" + pkg.name
    authors = scheming_load_json(pkg.author, None)
    if isinstance(authors, str):
        authors = [authors] if authors else []
    authors = set(authors)
    fullnames = helpers.authors_fullnames()
    authors = [fullnames[author] for author in authors]
    if authors:
        data[key] += ', '.join(authors) + " et al., "
    data[key] += str(pkg.metadata_modified.year) + ", " + \
                 pkg.name + ": COAT project data. " + \
                 "Available online: " + url

def _associated_datasets(data):
    context = {'ignore_auth': True}
    datasets = data.get(('datasets',), '')
    if datasets:
        for name in datasets.split(','):
            yield toolkit.get_action('ckan_package_show')(context, {'id': name})

def datasets_visibility(key, data, errors, context):
    if not str_to_bool(data[key]):
        for package in _associated_datasets(data):
            if package['private']:
                raise toolkit.Invalid('Cannot set a state variable as public '
                    'if one or more associated datasets are private')

def merge_from_datasets(key, data, errors, context, sep=","):
    values = set()
    for package in _associated_datasets(data):
        parts = package.get(key[0])
        if not parts:
            continue
        if type(parts) == str:
            parts = parts.split(sep)
        for part in parts:
            part = part.strip()
            if part:
                values.add(part)
    data[key] = sep.join(values)

def merge_tags_from_datasets(key, data, errors, context):
    # Extract tags from datasets
    tags = set()
    for package in _associated_datasets(data):
        for tag in package['tags']:
            if tag:
                tags.add(tag['name'])
    data[key] = ",".join(tags)
    # Remove old tags
    #for data_key in data.copy().keys():
    #    if data_key[0] == 'tags':
    #        del data[data_key]
    # Create new tags
    toolkit.get_validator('tag_string_convert')(key, data, errors, context)
