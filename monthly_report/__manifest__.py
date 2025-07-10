# -*- coding: utf-8 -*-
{
    'name': 'MonthlyWeekly Sale report',
    'description': 'Sale report',
    'version': '18.0.1.0',
    'data': [
        'views/res_config_settings_view.xml',
        'data/ir_cron_data.xml',
        'data/sale_report_template.xml',
        'report/sale_report.xml',
        'report/sale_report_pdf_template.xml',
    ],
    'depends': ['sale'],
    'installable': True,
    'auto_install': False,
}