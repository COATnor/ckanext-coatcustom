import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.coat.logic.action.create
import ckanext.coatcustom.logic.action.create
import ckanext.coat.logic.action.update
import ckanext.coatcustom.logic.action.update
import ckanext.coatcustom.helpers as helpers

import json
import requests

CKAN_SCHEMA = 'http://solr:8983/solr/ckan/schema'

class CoatcustomPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IValidators)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'coatcustom')
        self._custom_schema()

    def _custom_schema(self):
        response = requests.get(CKAN_SCHEMA+'/fields')
        fields = response.json()['fields']
        for name in "bbox_area maxx maxy minx miny".split():
            new_field = {
                "name": name,
                "type": "float",
                "indexed": "true",
                "stored": "true",
            }
            if new_field not in fields:
                requests.post(CKAN_SCHEMA, json={"add-field":new_field})

    # IValidators

    def get_validators(self):
        return {
            'str_to_bool': lambda s: str(s).lower() == "true",
            'multiple_to_json': lambda l: json.dumps(l) if l else "[]",
        }

    # IActions

    def get_actions(self):
        return {
                   'coat_package_create':
                       ckanext.coat.logic.action.create.package_create,
                   'package_create':
                       ckanext.coatcustom.logic.action.create.package_create,
                   'coat_package_update':
                       ckanext.coat.logic.action.update.package_update,
                   'package_update':
                       ckanext.coatcustom.logic.action.update.package_update,
        }

    # IFacets

    def _facets(self, facets_dict):
        if 'groups' in facets_dict:
            del facets_dict['groups']
        facets_dict['extras_location'] = toolkit._('Locations')
        facets_dict['organization'] = toolkit._('Modules')
        facets_dict['topic_category'] = toolkit._('Topic Category')
        return facets_dict

    def dataset_facets(self, facets_dict, package_type):
        return self._facets(facets_dict)

    # ITemplateHelpers

    def get_helpers(self):
        return { name:getattr(helpers, name) for name in dir(helpers) }
