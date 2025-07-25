# -*- coding: utf-8 -*-
{
    'name': 'Salesperson Filter',
    'description': 'creating search filter according to salesperson',
    'version':'1.0',
    'data': [
        'views/crm_lead_view.xml',
    ],
'assets': {
   'web.assets_backend': [
       'salesperson_filter/static/src/xml/salesperson_filter_list.xml',
       'salesperson_filter/static/src/js/salesperson_filter_list.js',
       # 'salesperson_filter/static/src/js/salesperson_search_filter.js',
   ],
},
    'depends': ['crm','base','web'],
    'installable':'True'
}
