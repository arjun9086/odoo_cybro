# -*- coding: utf-8 -*-
"""Settings report"""
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    """Settings options for sending report"""
    _inherit = 'res.config.settings'

    is_sale_report = fields.Boolean(string='Report Email', config_parameter='sale_report.is_sale_report')
    customer_ids = fields.Many2many('res.partner', string='Customer')
    sales_team_id = fields.Many2one('crm.team', string='Sales team', config_parameter='sale_report.sales_team_id')
    start_date = fields.Datetime(string="Start Date", config_parameter='sale_report.start_date')
    end_date = fields.Datetime(string="End Date", config_parameter='sale_report.end_date')
    method = fields.Selection(selection=[('weekly', 'Weekly'), ('monthly', 'Monthly'), ],
                              string='Method', default='weekly', config_parameter='sale_report.method')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        ir_config.set_param(
            'sale_report.customer_ids',
            ','.join(map(str, self.customer_ids.ids)) if self.customer_ids else '')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        customer_ids = ir_config.get_param('sale_report.customer_ids', default='')
        res.update(
            customer_ids=[(6, 0, list(map(int, customer_ids.split(','))))] if customer_ids else False,)
        return res
