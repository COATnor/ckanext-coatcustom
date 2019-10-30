import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.coat.logic.action.create
import ckanext.coatcustom.logic.action.create
import ckanext.coatcustom.helpers as helpers


class CoatcustomPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'coatcustom')

    def get_actions(self):
        return {
                   'coat_package_create':
                       ckanext.coat.logic.action.create.package_create,
                   'package_create':
                       ckanext.coatcustom.logic.action.create.package_create
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
