# -*- coding: utf-8 -*-
{
    'name': 'POS-Rating',
    'description': 'POS product rating',
    'version': '1.0',
    'data': [
        'views/product_product_view.xml',
        'views/res_config_settings_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos/static/src/xml/reached_limit_popup.xml',
            'pos/static/src/xml/pos_product_rating.xml',
            'pos/static/src/xml/pos_orderline_rating.xml',
            'pos/static/src/js/pos_store.js',
            'pos/static/src/js/reached_limit_popup.js',
        ],
    },
    'depends': ['point_of_sale', 'product'],
    'installable': 'True'
}
