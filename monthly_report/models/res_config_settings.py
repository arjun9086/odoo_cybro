# -*- coding: utf-8 -*-
"""Settings report"""
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    """Settings options for sending report"""
    _inherit = 'res.config.settings'

    is_sale_report = fields.Boolean(string='Report Email', config_parameter='sale_report.is_sale_report')
    customer_ids = fields.Many2many('res.partner', string='Customer')
    sales_team_id = fields.Many2one('crm.team', string='Sales team')
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    method = fields.Selection(selection=[('weekly', 'Weekly'), ('monthly', 'Monthly'), ],
                              string='Method')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        ir_config.set_param(
            'sale_report.customer_ids',
            ','.join(map(str, self.customer_ids.ids)) if self.customer_ids else '')
        ir_config.set_param(
            'sale_report.sales_team_id',
            self.sales_team_id.id if self.sales_team_id else '')
        ir_config.set_param(
            'sale_report.start_date',
            self.start_date.isoformat() if self.start_date else '')
        ir_config.set_param(
            'sale_report.end_date',
            self.end_date.isoformat() if self.end_date else '')
        ir_config.set_param(
            'sale_report.method',
            self.method or '')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        customer_ids = ir_config.get_param('sale_report.customer_ids', default='')
        sales_team_id = ir_config.get_param('sale_report.sales_team_id', default=False)
        start_date = ir_config.get_param('sale_report.start_date', default='')
        end_date = ir_config.get_param('sale_report.end_date', default='')
        method = ir_config.get_param('sale_report.method', default='')
        res.update(
            customer_ids=[(6, 0, list(map(int, customer_ids.split(','))))] if customer_ids else False,
            sales_team_id=int(sales_team_id) if sales_team_id else False,
            start_date=start_date or False,
            end_date=end_date or False,
            method=method or False
        )
        return res