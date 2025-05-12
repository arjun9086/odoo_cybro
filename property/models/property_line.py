# -*- coding: utf-8 -*-
"""utf8"""
from odoo import models, fields, api


class PropertyLine(models.Model):
    """class for Property_Property """
    _name = "property.line"

    name = fields.Char()
    property_id = fields.Many2one('property.property', string="Property")
    property_inverse_id = fields.Many2one("property.rental")
    rent = fields.Integer(related="property_id.rent", string="Rent")
    quantity_ = fields.Integer(string="Quantity", default=1)
    invoiced_qty = fields.Float(string='Invoiced quantity', default=0.0)
    subtotal = fields.Integer(string="Subtotal", compute='_compute_subtotal')

    def _compute_subtotal(self):
        """subtotal"""
        for line in self:
            line.subtotal = line.rent * line.quantity_
