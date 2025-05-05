# -*- coding: utf-8 -*-
"""utf8"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PropertyRental(models.Model):
    """Rental or Lease Management"""
    _name = "property.rental"
    _description = "Rental or Lease Management"
    _inherit = ['mail.thread']

    name = fields.Char(string="Sequence number", default=lambda self: 'New', readonly=True)
    type = fields.Selection(selection=[('rent', 'Rent'), ('lease', 'Lease')])
    property_id = fields.Many2one("property.property", string="Property")
    tenant_id = fields.Many2one("res.partner", string="Tenant")
    amount = fields.Integer(string="Amount")
    start_date = fields.Date(string="Period")
    end_date = fields.Date(string="End date")
    total_amount = fields.Integer(string="Total Amount", related="property_id.legal_amount")
    status = fields.Selection(
        selection=[('draft', 'Draft'), ('confirm', 'Confirmed'), ('closed', 'Closed'), ('returned', 'Returned'),
                   ('expired', 'Expired')],
        string='Status',
        default='draft',
        tracking=True)
    remaining_days = fields.Char(string="Remaining days", compute='_compute_remaining_days', store=True)
    company_id = fields.Many2one('res.company')

    # def invoice(self):
    #     """Invoice creation"""
    #     # self.env['account.move'].create([
    #     #     {'move_type': 'out_invoice'
    #     #      }
    #     # ])
    #     return


@api.model_create_multi
def create(self, vals_list):
    """Automatically generate a reference number for rental."""
    for vals in vals_list:
        if vals.get('name', 'New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('property.rental')
    return super(PropertyRental, self).create(vals_list)


@api.depends('end_date', 'start_date')
def _compute_remaining_days(self):
    """remaining date"""
    for record in self:
        if record.end_date and record.start_date:
            record.remaining_days = record.end_date - record.start_date
        else:
            record.remaining_days = 0


def confirm(self):
    """Confirm state"""
    if self.message_attachment_count != 0:
        self.write({'status': 'confirm'})
    else:
        raise ValidationError("At least 1 file must be attached")


def closed(self):
    """closed state"""
    self.write({'status': 'closed'})


def returned(self):
    """returned state"""
    self.write({'status': 'returned'})


def expire(self):
    """expire state"""
    self.write({'status': 'expired'})
