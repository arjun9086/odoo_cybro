# -*- coding: utf-8 -*-
{
    'name': 'Employee Dashboard',
    'version': '1.0',
    'description': 'Dashboard in Employee module',
    'data': [
        'views/employee_menu.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'employee_dashboard/static/src/js/dashboard.js',
            'employee_dashboard/static/src/xml/dashboard.xml',
            # 'employee_dashboard/static/src/lib/chart.js',
        ],
    },
    'depends': ['hr','project','base','hr_holidays','hr_org_chart'],
}
