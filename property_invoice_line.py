# -*- coding: utf-8 -*-
"""utf8"""
from email.policy import default

from odoo import models, fields,api


class PropertyLine(models.Model):
    """class for Invoice in property """
    _name = 'property.line'
    _description = 'Property Invoice'

    property_id=fields.Many2one('property.rental', string='Property')
    name=  fields.Many2one('property.property',string='Properties')
    rent = fields.Integer(related='name.rent')
    quantity=fields.Integer(default=1,string='Quantity')
    invoiced_qty = fields.Float(string="Invoiced Quantity", default=0.0)
    subtotal=fields.Integer(string='Subtotal',compute='compute_subtotal')

    @api.depends('quantity', 'rent')
    def compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.rent