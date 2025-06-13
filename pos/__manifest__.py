# -*- coding: utf-8 -*-
{
    'name': 'POS-Rating',
    'description': 'POS product rating',
    'version': '1.0',
    'data': [
        'views/product_product_view.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos/static/src/xml/pos_product_rating.xml',
        ],
    },
    'depends': ['sale', 'point_of_sale', 'product'],
    'installable': 'True'
}
