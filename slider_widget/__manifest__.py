# -*- coding: utf-8 -*-
{
    'name': 'Range Slider Widget',
    'description': ' Get values using slider widget',
    'version': '1.0',
    'data': [
        'views/property_property_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'slider_widget/static/src/js/range_slider.js',
            'slider_widget/static/src/xml/range_slider_template.xml',
        ],
    },
    'depends': ['property'],
    'installable': 'True'
}