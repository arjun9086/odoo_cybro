# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PropertyRental(models.Model):
    """Rental or Lease Management"""
    _name = "property.rental"
    _description = "Rental or Lease Management"
    _inherit = ['mail.thread']

    type = fields.Selection(required=True, selection=[('rent', 'Rent'), ('lease', 'Lease')])
    property_id = fields.Many2one("property.property", string="Property")
    tenant_id = fields.Many2one("res.partner", string="Tenant")
    amount = fields.Integer(string="Rent Amount")
    start_date = fields.Date(string="Period", default=fields.Date.context_today)
    end_date = fields.Date(string="End date")
    total_amount = fields.Integer(string="Total_amount", related="property_id.legal_amount")
    status = fields.Selection(
        selection=[('draft', 'Draft'), ('confirm', 'Confirmed'), ('closed', 'Closed'), ('returned', 'Returned'),
                   ('expired', 'Expired')],
        string='Status',
        default='draft',
        tracking=True
    )
    attachment = fields.Binary(required=True)
    remaining_days = fields.Char(string="Remaining days", compute='_compute_remaining_days', store=True)
    company = fields.Many2one('res.company')
    reference_number = fields.Char(default=lambda self: 'New', readonly=True, copy=False,
                                   help="Reference Number of Rent")

    @api.model
    def create(self, vals):
        """Automatically generate a reference number for new rental."""
        if vals.get('reference_number', 'New' == 'New'):
            vals['reference_number'] = self.env['ir.sequence'].next_by_code('property.rental')
        return super(PropertyRental, self).create(vals)

    @api.depends('end_date', 'start_date')
    def _compute_remaining_days(self):
        for record in self:
            if record.end_date and record.start_date:
                remaining_day = record.end_date - record.start_date
                record.remaining_days = remaining_day
            else:
                record.remaining_days = 0

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
