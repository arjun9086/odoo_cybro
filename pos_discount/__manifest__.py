{
    'name': 'POS Session Discount Limit',
    'version': '18.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Set a maximum discount limit per POS session',
    'description': """
        This module allows setting a maximum discount limit for a POS session
        and prevents applying discounts beyond the limit.
    """,
    # 'author': 'Arjun',
    'depends': ['point_of_sale', 'product'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/pos_config_views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_discount/static/src/js/discount_limit.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}