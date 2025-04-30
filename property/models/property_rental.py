# -*- coding: utf-8 -*-

from odoo import models, fields


class PropertyRental(models.Model):
    """Rental or Lease Management"""
    _name = "property.rental"
    _description = "Rental or Lease Management"
    _inherit = ['mail.thread']

    name = fields.Char(related="property_id.name")
    type = fields.Selection(selection=[('rent', 'Rent'), ('lease', 'Lease')])
    property_id = fields.Many2one("property.property", string="Property")
    tenant_id = fields.Many2one("res.partner", string="Tenant")
    amount = fields.Integer(string="Rent Amount")
    start_date = fields.Datetime(string="Period", default=fields.Date.context_today)
    end_date = fields.Datetime(string="End date")
    total_amount = fields.Integer(string="Total_amount", related="property_id.legal_amount")
    status = fields.Selection(
        selection=[('draft', 'Draft'), ('confirm', 'Confirmed'), ('closed', 'Closed'), ('returned', 'Returned'),
                   ('expired', 'Expired')],
        string='Status',
        default='draft',
        tracking=True
    )
    attachment = fields.Binary(required=True)
    days=fields.Datetime()
    def confirm(self):
        self.write({'status': 'confirm'})
        return

    def closed(self):
        self.write({'status': 'closed'})
        return

    def returned(self):
        self.write({'status': 'returned'})
        return

    def expire(self):
        self.write({'status': 'expired'})
        return
