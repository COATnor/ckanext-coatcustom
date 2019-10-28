import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.coat.logic.action.create
import ckanext.coatcustom.logic.action.create


class CoatcustomPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IActions)

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

    '''
               # IPackageController
    @toolkit.side_effect_free
    @toolkit.chained_action
    def after_create(self, context, data_dict):
        # t = get_or_bust(data_dict, 'type')
        # expanded = data_dict.get('expanded', True)
        # s = scheming_get_dataset_schema(t, expanded)

        # data_dict['extras'].append({'key':'spatial', 'value':'test'})
        # import pdb;
        # pdb.set_trace()
        # package_update(context, data_dict)
        if data_dict.get('__parent', False):
            return

        #import pdb;pdb.set_trace()

        if 'extras' not in data_dict:
            data_dict['extras'] = []

        value = 'test'
        for extra in data_dict['extras']:
            if extra['key'] == 'spatial':
                extra['value'] = value
                break
        else:
            data_dict['extras'].append({'key': 'spatial', 'value': value})

        data_dict['spatial'] = value
        #import pdb;
        #pdb.set_trace()
        toolkit.get_action('package_update')(context, data_dict)
        
'''