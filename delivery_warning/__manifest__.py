# -*- coding: utf-8 -*-
{
    'name': 'Delivery Warning',
    'description': 'Delivery Warning on Sale order',
    'version':'1.0',
    'data': [
        'views/sale_order_view.xml',
        'views/stock_picking_view.xml',
        'views/report_stockpicking_operations.xml',
        'views/delivery_warning_sale_portal.xml',
    ],
    'depends': ['sale','stock','sale_stock'],
    'installable':'True'
}
