# -*- coding: utf-8 -*-
"""inheriting property_property model"""
from odoo import models, fields

class PropertyProperty(models.Model):
    _inherit = 'property.property'

    quality_mark = fields.Integer(string='Quality')
