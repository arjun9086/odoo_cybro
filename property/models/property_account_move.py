# -*- coding: utf-8 -*-
"""utf8"""
from odoo import models, fields


class AccountMove(models.Model):
    """class for Invoice in property """
    _inherit = ['account.move']
    _description = 'Property Invoice'

    property_ids1 = fields.Many2many('property.rental', string='Property')
    property_ids2 = fields.Many2many(related="property_ids1.property_ids")
