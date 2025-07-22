# -*- coding: utf-8 -*-
{
    'name': 'Import customers',
    'description': 'importing customer from old database to new',
    'version':'1.0',
    'data': [
        'views/contact_view.xml',
        'wizard/customer_import.xml',
    ],
    'depends': ['base'],
    'installable':'True'
}
