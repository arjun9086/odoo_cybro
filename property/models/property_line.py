# -*- coding: utf-8 -*-
"""utf8"""
from odoo import models, fields, api


class PropertyLine(models.Model):
    """class for Property_Property """
    _name = "property.line"
    _description = "Lines of property"

    property_id = fields.Many2one('property.property', string="Property")
    property_inverse_id = fields.Many2one("property.rental")
    rent = fields.Integer(related="property_id.rent", string="Rent")
    quantity_ = fields.Float(related='property_inverse_id.remaining_days', string="Quantity")
    invoiced_qty = fields.Float(string='Invoiced quantity', default=0.0)
    subtotal = fields.Integer(string="Subtotal", compute='_compute_subtotal', store=True)
    invoice_line_ids = fields.Many2many("account.move.line", string='Linked field')

    def _compute_subtotal(self):
        """subtotal"""
        for line in self:
            line.subtotal = line.rent * line.quantity_
