import logging

import ckan
import ckan.plugins as p
import ckan.logic as logic
import ckan.lib.helpers as h

import re

log = logging.getLogger(__name__)

def build_nav_main_lamma(*args):
    ''' build a set of menu items.

    args: tuples of (menu type, title) eg ('login', _('Login'))
    outputs <li><a href="...">title</a></li>
    '''
    output = ''
    for item in args:
        menu_item, title = item[:2]
        if len(item) == 3 and not h.check_access(item[2]):
            continue
        output += _make_menu_item_lamma(menu_item, title)
    return output
	
def _make_menu_item_lamma(menu_item, title, **kw):
    ''' build a navigation item used for example breadcrumbs

    outputs <li><a href="..."></i> title</a></li>

    :param menu_item: the name of the defined menu item defined in
    config/routing as the named route of the same name
    :type menu_item: string
    :param title: text used for the link
    :type title: string
    :param **kw: additional keywords needed for creating url eg id=...

    :rtype: HTML literal

    This function is called by wrapper functions.
    '''
    _menu_items = h.config['routes.named_routes']
    if menu_item not in _menu_items:
        raise Exception('menu item `%s` cannot be found' % menu_item)
    item = h.copy.copy(_menu_items[menu_item])
    item.update(kw)
    active = h._link_active(item)
    needed = item.pop('needed')
    for need in needed:
        if need not in kw:
            raise Exception('menu item `%s` need parameter `%s`'
                            % (menu_item, need))
    link = h._link_to(title, menu_item, suppress_active_class=True, **item)
    
    ##log.info('::::::::::::::::::::::::::: %r', menu_item)
	
    if active:
        return h.literal('<li class="active_lamma">') + link + h.literal('</li>')
    
    if menu_item == "search": 
 	return h.literal('<li class="blue_bg">') + link + h.literal('</li>')
    if menu_item == "organizations_index":
	return h.literal('<li class="blue_bg">') + link + h.literal('</li>')	

    return h.literal('<li class="green_bg">') + link + h.literal('</li>')

def lamma_groups_available():
    '''
    Return a list of the groups.
    '''

    context = {}
    data_dict = {'sort': 'packages', 'all_fields': 1}
    return logic.get_action('group_list')(context, data_dict)

def get_full_groups_facetslist(fname, facets):
    '''
	Return a complete list of groups facet.
    '''
    ##log.info('FACET_NAME::::::::::::::::::::::::::: %r', fname)
	
    context = {}
    data_dict = {'sort': 'packages', 'all_fields': 1}
    groups = logic.get_action('group_list')(context, data_dict)
	
    ##log.info('GROUPS::::::::::::::::::::::::::: %r', groups)

    fnames = []
    for facet in facets:
        fnames.append(facet['display_name'])
    	##log.info('::::::::::::::::::::::::::: %r', facet['display_name'])
	
    for group in groups:
	##log.info('::::::::::::::::::::::::::: %r', group)
    	d_name = group['display_name']

        ##log.info('GROUP_NAME::::::::::::::::::::::::::: %r', d_name)
	
	if d_name not in fnames:
	        new_facet = {
        	       'display_name': d_name,
                       'count': 0,
                       'active': False,
		       'disabled': True,
                       'name': group['name']
                }

		facets.append(new_facet)

    ##
    ## ORDER the Facets by cat number
    ##    

    ##log.info('FACETS::::::::::::::::::::::::::: %r', facets)

    for facet in facets:
	cat_number = str(facet['name'])
	cat_number = re.findall("\d+", cat_number)
	##log.info('CATNUMBER::::::::::::::::::::::::::: %r', cat_number[0])
        facet['number'] = int(cat_number[0])

    ##log.info('FACETS::::::::::::::::::::::::::: %r', facets)

    facets = sorted(facets, key=lambda item: item['number'])

    ##log.info('FACETS::::::::::::::::::::::::::: %r', facets)

    return facets
