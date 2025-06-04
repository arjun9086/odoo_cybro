# -*- coding: utf-8 -*-
{
    'name': 'Property Management',
    'version': '1.0',
    'description': 'Property Management',
    'data': [
        'security/ir.model.access.csv',
        'security/property_groups.xml',
        'security/rental_groups.xml',
        'security/ir_rule.xml',
        'views/property_property_view.xml',
        'views/property_rental_view.xml',
        'views/property_facility_view.xml',
        'views/account_move_view.xml',
        'views/res_partner_view.xml',
        'views/property_website_view.xml',
        'views/rental_website_view.xml',
        'data/email_template_data.xml',
        'data/ir_cron.xml',
        'data/late_payment_template.xml',
        'wizard/report_wizard_view.xml',
        'reports/property_report.xml',
        'reports/property_report_templates.xml',
        'views/property_menu.xml'],
    'depends': ['base', 'mail', 'account', 'sale','website'],
'assets': {
        'web.assets_backend': [
            'property/static/src/js/action_manager.js',],
}
}
