import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

class LammaThemePlugin(plugins.SingletonPlugin):
        '''An example theme plugin.

        '''
        # Declare that this class implements IConfigurer.
        plugins.implements(plugins.IConfigurer)
	plugins.implements(plugins.ITemplateHelpers)

        def update_config(self, config):

                # Add this plugin's templates dir to CKAN's extra_template_paths, so
                # that CKAN will use this plugin's custom templates.
                toolkit.add_template_directory(config, 'templates')

                # Add this plugin's public dir to CKAN's extra_public_paths, so
                # that CKAN will use this plugin's custom static files.
                toolkit.add_public_directory(config, 'public')
				
        def get_helpers(self):

        	from ckanext.lamma import helpers as lamma_helpers
        	return {
                	'build_nav_main_lamma': lamma_helpers.build_nav_main_lamma,
			'_make_menu_item_lamma': lamma_helpers._make_menu_item_lamma,
 	       	}
