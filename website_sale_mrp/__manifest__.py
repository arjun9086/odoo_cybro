# -*- coding: utf-8 -*-
{
    'name': 'Website sale mrp',
    'description': 'ecommerce shop in odoo website',
    'version': '18.0.1.0',
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_config_settings_view.xml',
        'views/website_sale_view.xml',
    ],
    'depends': ['base','mrp', 'website_sale', 'website'],
    'installable': True,
    'auto_install': False,
}
