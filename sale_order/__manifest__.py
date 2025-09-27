# -*- coding: utf-8 -*-
{
    'name': 'Sale Order',
    'description': 'Sale order line',
    'version':'1.0',
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'wizard/import_file_wiz.xml',
    ],
    'depends': ['sale'],
    'installable':'True'
}
