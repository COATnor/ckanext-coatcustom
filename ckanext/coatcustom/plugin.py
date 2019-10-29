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
        self._create_coat_vocabulary()

    def _create_coat_vocabulary():
        '''Create the COAT vocabulary, and populate with custom tags, if they don't exist already.

        Note that you could also create the vocab and tags using CKAN's API,
        and once they are created you can edit them (e.g. to add and remove
        possible TAG values) using the API.

        '''
        user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
        context = {'user': user['name']}
        try:
            data = {'name': 'coat_vocabulary'}
            toolkit.get_action('vocabulary_show')(context, data)
        except toolkit.ObjectNotFound:
            data = {'name': 'coat_vocabulary'}
            vocab = toolkit.get_action('vocabulary_create')(context, data)
            for tag in (u'tall shrub',
                        u'forest',
                        u'birch forest',
                        u'tundra',
                        u'meadow',
                        u'heath',
                        u'dwarf shrub heath',
                        u'snow beds',
                        u'moss tundra',
                        u'grassy tundra',
                        u'hummock tundra',
                        u'point intercept',
                        u'camera traps',
                        u'snow tracking',
                        u'surveys',
                        u'experimental exclosures',
                        u'remote sensing',
                        u'satellite imagery',
                        u'aerial imagery',
                        u'repeat photography',
                        u'flight intercept traps',
                        u'snap trapping',
                        u'pellet counts',
                        u'GPS tags',
                        u'satellite tags',
                        u'stable isotopes',
                        u'dendroecology',
                        u'hunting records',
                        u'metabarcoding',
                        u'barcoding',
                        u'microsatellites',
                        u'scat analysis',
                        u'NDVI',
                        u'albedo',
                        u'modelling',
                        u'snow modelling',
                        u'population modelling',
                        u'temperature logger',
                        u'weather station',
                        u'snow pits',
                        u'NIRS',
                        u'distance sampling',
                        u'live trapping',
                        u'artificial nests',
                        u'snow depth',
                        u'snow structure',
                        u'temperature',
                        u'air temperature',
                        u'ground temperature',
                        u'soil temperature',
                        u'precipitation',
                        u'wind',
                        u'ground ice',
                        u'icing',
                        u'humidity',
                        u'ice thickness',
                        u'timing of snow melt',
                        u'timing of icing',
                        u'snow melt',u'rain on snow',
                        u'radiation'
                        ):
                tag_entry = {'name': tag, 'vocabulary_id': vocab['id']}
                toolkit.get_action('tag_create')(context, tag_entry)


    def get_actions(self):
        return {
                   'coat_package_create':
                       ckanext.coat.logic.action.create.package_create,
                   'package_create':
                       ckanext.coatcustom.logic.action.create.package_create
        }