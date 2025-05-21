# -*- coding: utf-8 -*-
"""utf8"""
from odoo import models, fields


class PropertyLine(models.Model):
    """class for Property_Property """
    _name = "property.line"
    _description = "Lines of property"

    property_id = fields.Many2one('property.property', string="Property")
    property_inverse_id = fields.Many2one("property.rental", string="Inverse")
    rent = fields.Integer(related="property_id.rent", string="Rent")
    quantity_ = fields.Float(related='property_inverse_id.remaining_days', string="Quantity")
    subtotal = fields.Integer(string="Subtotal", compute='_compute_subtotal')
    invoice_line_ids = fields.Many2many("account.move.line", string='Linked field')

    def _compute_subtotal(self):
        """subtotal"""
        for line in self:
            line.subtotal = line.rent * line.quantity_

    def link_invoice_lines(self, invoice):
        """link of invoice lines """
        for line in self:
            matched_lines = invoice.invoice_line_ids.filtered(lambda l: l.name == line.property_id.name)
            line.invoice_line_ids |= matched_lines
