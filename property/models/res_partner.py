# -*- coding: utf-8 -*-
"""utf8"""
from odoo import models, fields


class ResPartner(models.Model):
    """class for Invoice in property """
    _inherit = ['res.partner']
    _description = 'Partner Invoice'

    property_ids = fields.One2many('property.property', 'owner_id', readonly=True)